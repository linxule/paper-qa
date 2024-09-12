import streamlit as st

st.title("Help and Documentation")

st.write("""
## PaperQA2 Web App Help

This application allows you to manage your research papers, ask questions about them, and visualize the relationships between documents.

### Main Features:

1. **Document Management**: Load PDFs, save and load databases with embeddings.
2. **Ask Questions**: Query your document collection using advanced language models.
3. **Search and Visualize**: Search your documents and visualize citation networks.
4. **Query History**: View and export your past queries.
5. **Settings**: Customize default settings for the application.

### Tips:

- Start by loading your PDF documents in the Document Management page.
- Use the Settings page to set your preferred default values for models and parameters.
- The Ask Questions page allows both single queries and batch processing.
- You can visualize the relationships between your documents in the Search and Visualize page.
- Export your query history for future reference.

For more detailed information, please refer to the [PaperQA2 documentation](https://github.com/whitead/paper-qa).
""")

st.subheader("Frequently Asked Questions")

faq = {
    "How do I get started?": "Begin by loading your PDF documents in the Document Management page. Then, you can start asking questions about your documents in the Ask Questions page.",
    "Can I save my progress?": "Yes, you can save your database with embeddings in the Document Management page. This allows you to quickly reload your documents and their associated data in future sessions.",
    "How do I customize the model settings?": "You can adjust the model settings in the sidebar of the Ask Questions page. For default settings, use the Settings page.",
    "What if I have multiple questions?": "You can use the batch processing feature in the Ask Questions page to ask multiple questions at once.",
    "How can I visualize the relationships between my documents?": "The Search and Visualize page offers a citation network visualization feature.",
}

for question, answer in faq.items():
    with st.expander(question):
        st.write(answer)