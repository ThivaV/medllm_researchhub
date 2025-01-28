import io
import streamlit as st
from dataclasses import dataclass

@dataclass
class Report:
    file_id: str
    file_name: str
    file_type: str
    is_file_attached: bool = False
    file_io_bytes: any = None

def upload_files():
    """Upload files"""

    # Initialize uploaded reports list
    reports = []

    # File uploader for both images and PDFs
    uploaded_files = st.file_uploader(
        "Choose files...",
        type=["jpg", "png", "jpeg", "pdf"],
        accept_multiple_files=True,
    )

    for uploaded_file in uploaded_files:
        report_id = uploaded_file.file_id
        report_name = uploaded_file.name
        report_type = uploaded_file.type
        report_attached = False
        report_io_bytes = io.BytesIO(uploaded_file.getvalue())

        report = Report(report_id, report_name, report_type, report_attached, report_io_bytes)
        reports.append(report)

    st.session_state.reports = reports