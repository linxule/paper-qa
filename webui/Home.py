import streamlit as st
from webui.utils import initialize_session_state

st.set_page_config(page_title="PaperQA2 Web App", layout="wide")
initialize_session_state()

st.title("PaperQA2 Web App")

st.write("""
Welcome to the PaperQA2 Web App! This application allows you to manage your research papers,
ask questions about them, and visualize the relationships between documents.

Use the sidebar to navigate between different features:
- Ask Questions: Query your document collection
- Document Management: Load, save, and view your document database
- Search and Visualize: Search your documents and visualize citation networks
- Query History: View and export your past queries

Get started by loading your PDF documents in the Document Management page.
""")

# Display some basic stats
st.subheader("Current Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Documents", len(st.session_state.docs.docs))
col2.metric("Total Queries", len(st.session_state.query_history))
col3.metric("API Usage - Queries", st.session_state.api_usage['queries'])
col4.metric("API Usage - Tokens", st.session_state.api_usage['tokens'])