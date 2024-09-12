import streamlit as st
import os
import pickle
import datetime
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from paperqa import Docs, Settings, ask
from paperqa import HybridEmbeddingModel, SparseEmbeddingModel, LiteLLMEmbeddingModel
from pypdf import PdfReader

# Ensure you have the latest versions installed:
# pip install -U streamlit pypdf paper-qa networkx matplotlib pandas

# Initialize session state
if 'docs' not in st.session_state:
    st.session_state.docs = Docs()
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'api_usage' not in st.session_state:
    st.session_state.api_usage = {'queries': 0, 'tokens': 0}
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {}

def load_docs(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    num_pages = len(reader.pages)
                st.session_state.docs.add(file_path)
                st.write(f"Loaded {file} ({num_pages} pages)")
            except Exception as e:
                st.error(f"Error loading {file}: {str(e)}")

def save_docs(docs, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(docs, f)

def load_saved_docs(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def save_user_settings():
    st.session_state.user_settings = {
        'llm_model': llm_model,
        'embedding_model': embedding_model,
        'k': k,
        'max_sources': max_sources,
        'qa_prompt': qa_prompt
    }

def load_user_settings():
    if st.session_state.user_settings:
        return st.session_state.user_settings
    return {}

st.set_page_config(page_title="PaperQA2 Web App", layout="wide")

st.title("PaperQA2 Web App")

# Sidebar for settings and database management
with st.sidebar:
    st.header("Settings")
    pdf_folder = st.text_input("PDF Folder Path")
    db_file = st.text_input("Database File Path", "my_docs.pkl")

    if st.button("Load PDFs"):
        if pdf_folder:
            with st.spinner("Loading PDFs..."):
                load_docs(pdf_folder)
            st.success(f"Loaded PDFs from {pdf_folder}")

    if st.button("Save Database"):
        if db_file:
            with st.spinner("Saving database..."):
                save_docs(st.session_state.docs, db_file)
            st.success(f"Saved database to {db_file}")

    if st.button("Load Database"):
        if db_file and os.path.exists(db_file):
            with st.spinner("Loading database..."):
                st.session_state.docs = load_saved_docs(db_file)
            st.success(f"Loaded database from {db_file}")

    # Load user settings
    user_settings = load_user_settings()

    # Model Settings
    st.subheader("Model Settings")
    llm_model = st.selectbox("LLM Model", ["gpt-4o-2024-08-06", "gpt-4o-mini", "claude-3-5-sonnet-20240620"], index=["gpt-4o-2024-08-06", "gpt-4o-mini", "claude-3-5-sonnet-20240620"].index(user_settings.get('llm_model', "gpt-4o-2024-08-06")))
    embedding_model = st.selectbox("Embedding Model", ["text-embedding-3-small", "text-embedding-3-large", "hybrid-text-embedding-3-small", "sparse"], index=["text-embedding-3-small", "text-embedding-3-large", "hybrid-text-embedding-3-small", "sparse"].index(user_settings.get('embedding_model', "text-embedding-3-small")))

    # Customize number of sources
    k = st.slider("Number of top passages (k)", 1, 10, user_settings.get('k', 5))
    max_sources = st.slider("Max sources for final answer", 1, 5, user_settings.get('max_sources', 3))

    # Customize prompts
    st.subheader("Customize Prompts")
    qa_prompt = st.text_area("QA Prompt", user_settings.get('qa_prompt', "Answer the question '{question}' Use the context below if helpful. You can cite the context using the key like (Example2012).\n\nContext: {context}\n\n"))

    if st.button("Save Settings"):
        save_user_settings()
        st.success("Settings saved successfully!")

# Function to create custom embedding model
def get_embedding_model(model_name):
    if model_name.startswith("hybrid-"):
        return HybridEmbeddingModel(models=[LiteLLMEmbeddingModel(model_name=model_name[7:]), SparseEmbeddingModel(ndim=1024)])
    elif model_name == "sparse":
        return SparseEmbeddingModel(ndim=1024)
    else:
        return LiteLLMEmbeddingModel(model_name=model_name)

# Main app area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Ask a Question")
    query = st.text_input("Enter your question:")
    
    if st.button("Ask"):
        if query:
            with st.spinner("Generating answer..."):
                settings = Settings(
                    paper_directory=pdf_folder,
                    llm=llm_model,
                    embedding=get_embedding_model(embedding_model),
                    answer={"k": k, "answer_max_sources": max_sources},
                    prompts={"qa": qa_prompt}
                )
                answer = ask(query, settings=settings)
            st.markdown(answer.formatted_answer)
            st.session_state.query_history.append((datetime.datetime.now(), query, answer.formatted_answer))
            st.session_state.api_usage['queries'] += 1
            st.session_state.api_usage['tokens'] += len(query.split()) + len(answer.formatted_answer.split())

    # Add typewriter callback
    if st.toggle("Enable typewriter output"):
        st.write("Answer:")
        output = st.empty()
        
        def typewriter(chunk: str) -> None:
            output.write(output.text + chunk)
        
        if st.button("Ask (with typewriter)"):
            if query:
                settings = Settings(
                    paper_directory=pdf_folder,
                    llm=llm_model,
                    embedding=get_embedding_model(embedding_model),
                    answer={"k": k, "answer_max_sources": max_sources},
                    prompts={"qa": qa_prompt}
                )
                answer = ask(query, settings=settings, callbacks=[typewriter])
                st.session_state.query_history.append((datetime.datetime.now(), query, answer.formatted_answer))
                st.session_state.api_usage['queries'] += 1
                st.session_state.api_usage['tokens'] += len(query.split()) + len(answer.formatted_answer.split())

with col2:
    st.subheader("Database Statistics")
    st.metric("Total documents", len(st.session_state.docs.docs))
    st.metric("Total queries", len(st.session_state.query_history))
    st.metric("API Usage - Queries", st.session_state.api_usage['queries'])
    st.metric("API Usage - Tokens", st.session_state.api_usage['tokens'])

# Display loaded documents
st.subheader("Loaded Documents")
for doc in st.session_state.docs.docs:
    with st.expander(f"{doc.docname}"):
        st.write(f"Citation: {doc.citation}")
        st.write(f"Number of pages: {doc.num_pages}")

# Advanced Search functionality
st.subheader("Advanced Search")
search_query = st.text_input("Search for papers:")
date_range = st.date_input("Date range", [datetime.date(2020, 1, 1), datetime.date.today()])
if st.button("Search"):
    if search_query:
        results = [doc for doc in st.session_state.docs.docs if search_query.lower() in doc.docname.lower()]
        for doc in results:
            with st.expander(f"{doc.docname}"):
                st.write(f"Citation: {doc.citation}")
                st.write(f"Number of pages: {doc.num_pages}")

# Query History
st.subheader("Query History")
for date, q, a in reversed(st.session_state.query_history):
    with st.expander(f"{date.strftime('%Y-%m-%d %H:%M:%S')} - {q}"):
        st.markdown(a)

# Export functionality
st.subheader("Export Data")
if st.button("Export Query History"):
    df = pd.DataFrame(st.session_state.query_history, columns=['Date', 'Query', 'Answer'])
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="query_history.csv",
        mime="text/csv",
    )

# Simple Citation Network Visualization
st.subheader("Citation Network")
if st.button("Generate Citation Network"):
    G = nx.Graph()
    for doc in st.session_state.docs.docs:
        G.add_node(doc.docname)
        # This is a placeholder. In a real scenario, you'd need to parse citations from the documents
        for other_doc in st.session_state.docs.docs:
            if other_doc != doc and np.random.random() < 0.2:  # 20% chance of citation for demonstration
                G.add_edge(doc.docname, other_doc.docname)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=8, font_weight='bold', ax=ax)
    st.pyplot(fig)