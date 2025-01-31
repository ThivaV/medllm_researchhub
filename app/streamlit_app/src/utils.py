import io
import os
import base64
import tempfile

import streamlit as st

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

from src.groq_ops import chat


def upload_files():
    """Upload files"""

    # File uploader for both images and PDFs
    uploaded_files = st.file_uploader(
        "Choose files...",
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
    )

    if not st.session_state.groq_apikey:
        st.info("👈 :red[Please enter your Groq API Key] ⛔")
        st.stop()

    if not st.session_state.hf_apikey:
        st.info("👈 :red[Please enter your HuggingFace API Key] ⛔")
        st.stop()

    if not uploaded_files:
        st.info("👈 :red[Please upload patient reports] ⛔")
        st.stop()

    return uploaded_files


@st.cache_resource(ttl="1h")
def __initialize_embeddings():
    """Initialize embeddings"""

    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=st.session_state.hf_apikey,
        model_name="BAAI/bge-base-en-v1.5",
    )

    return embeddings


def __initialize_documents(uploaded_files):
    """Initialize documents"""

    docs = []
    for file in uploaded_files:
        if file.type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())

            loader = PyPDFLoader(temp_file.name, extract_images=True)

            # Extract text from the PDF
            pdf_contents = loader.load()

            docs.extend(pdf_contents)

            # Clean up the temp file
            os.unlink(temp_file.name)
        else:
            img_base64 = base64.b64encode(file.getvalue()).decode("utf-8")
            msg = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze the provided medical report and perform the following tasks: 
                                        1. Identification: Describe the key features or abnormalities visible in the report. 
                                        2. Prognosis: Suggest potential implications or diagnoses based on the identified features (if applicable). 
                                        3. Description: Provide a detailed summary of the observed structures, focusing on medical relevance.""",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}",
                            },
                        },
                    ],
                },
            ]

            img_contents = chat(msg)
            temp_docs = [Document(page_content=img_contents)]

            docs.extend(temp_docs)

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )
    documents = splitter.split_documents(docs)

    return documents


def __get_initial_summary(docs):
    """get report's summary after document upload"""

    context_parts = [doc.page_content for doc in docs]
    context = "\n\n".join(context_parts)

    prompt_template = """
    System Instruction: You are a helpful AI assistant with expertise in biomedical information analysis. 
    Using the provided context generated from patient medical reports, generate a summary that comprehensively analyzes the given information.

    Context: {context}
    """

    prompt = prompt_template.format(context=context)
    message = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    response = chat(message)

    return response


def initialize_retriever(uploaded_files, k: int = 5):
    """Initialize retriever"""

    # retrieve k
    k = k

    # retrieve documents
    documents = __initialize_documents(uploaded_files)

    # get summary about the reports uploaded
    report_summary = __get_initial_summary(documents)

    # embeddings
    embeddings = __initialize_embeddings()

    # vector retriever
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": k})

    # semantic retriever
    semantic_retriever = BM25Retriever.from_documents(documents)
    semantic_retriever.k = k

    # ensemble retriever
    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, semantic_retriever], weights=[0.5, 0.5]
    )

    return report_summary, ensemble_retriever
