import streamlit as st
import os
import pandas as pd
from pypdf import PdfReader
from webui.utils import save_docs_with_embeddings, load_docs_with_embeddings

st.title("Document Management")

pdf_folder = st.text_input("PDF Folder Path")
db_file = st.text_input("Database File Path", "my_docs.pkl")

if st.button("Load PDFs"):
    if pdf_folder:
        with st.spinner("Loading PDFs..."):
            for file in os.listdir(pdf_folder):
                if file.endswith('.pdf'):
                    file_path = os.path.join(pdf_folder, file)
                    try:
                        with open(file_path, 'rb') as f:
                            reader = PdfReader(f)
                            num_pages = len(reader.pages)
                        st.session_state.docs.add(file_path)
                        st.write(f"Loaded {file} ({num_pages} pages)")
                    except Exception as e:
                        st.error(f"Error loading {file}: {str(e)}")
        st.success(f"Loaded PDFs from {pdf_folder}")

if st.button("Save Database with Embeddings"):
    if db_file:
        with st.spinner("Saving database..."):
            save_docs_with_embeddings(st.session_state.docs, db_file)
        st.success(f"Saved database with embeddings to {db_file}")

if st.button("Load Database with Embeddings"):
    if db_file and os.path.exists(db_file):
        with st.spinner("Loading database..."):
            st.session_state.docs = load_docs_with_embeddings(db_file)
        st.success(f"Loaded database with embeddings from {db_file}")

st.subheader("Loaded Documents")
if st.session_state.docs.docs:
    df = pd.DataFrame([
        {
            "Document Name": doc.docname,
            "Citation": doc.citation,
            "Number of Pages": doc.num_pages
        } for doc in st.session_state.docs.docs
    ])
    st.dataframe(
        df,
        column_config={
            "Document Name": st.column_config.TextColumn("Document Name", width="medium"),
            "Citation": st.column_config.TextColumn("Citation", width="large"),
            "Number of Pages": st.column_config.NumberColumn("Number of Pages", format="%d")
        },
        hide_index=True,
    )
else:
    st.write("No documents loaded yet.")