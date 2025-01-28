import streamlit as st # type: ignore
from src import main

if __name__ == "__main__":
    st.set_page_config(page_title="BioMED", page_icon="⚕️", layout="wide")
    st.image("./docs/img/biomed_banner.png")
    main.initialize()
