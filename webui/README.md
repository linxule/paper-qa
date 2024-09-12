# PaperQA2 Web App

This is a Streamlit-based web application for PaperQA2, allowing users to manage research papers, ask questions about them, and visualize relationships between documents.

## Setup

1. Install the required packages:
   ```
   pip install -U streamlit pypdf paper-qa networkx matplotlib pandas
   ```

2. Navigate to the `my_paperqa_app` directory.

3. Run the Streamlit app:
   ```
   streamlit run webui/Home.py
   ```

## Features

- Document Management: Load, save, and view your document database
- Ask Questions: Query your document collection
- Search and Visualize: Search your documents and visualize citation networks
- Query History: View and export your past queries

## Usage

1. Start by loading your PDF documents in the Document Management page.
2. Use the sidebar to navigate between different features.
3. Customize model settings and prompts in the sidebar.

For more detailed information, refer to the PaperQA2 documentation.