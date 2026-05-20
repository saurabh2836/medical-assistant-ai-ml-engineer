import streamlit as st
from utils.api import upload_pdfs_api



def render_uploader():
    st.sidebar.header(f"Upload Medical documents (.PDFS)")
    uploaded_files= st.file_uploader("Upload multiple PDF's",type="pdf",accept_multiple_files=True)
    if st.sidebar.button("Upload DB") and uploaded_files:
        response=upload_pdfs_api(uploaded_files)
        if response.status_code ==200:
            st.sidebar.success("Uploaded successfully")