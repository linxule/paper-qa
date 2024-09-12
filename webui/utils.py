import streamlit as st
import os
import pickle
from paperqa import Docs, HybridEmbeddingModel, SparseEmbeddingModel, LiteLLMEmbeddingModel

def initialize_session_state():
    if 'docs' not in st.session_state:
        st.session_state.docs = Docs()
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    if 'api_usage' not in st.session_state:
        st.session_state.api_usage = {'queries': 0, 'tokens': 0}
    if 'user_settings' not in st.session_state:
        st.session_state.user_settings = {}

def get_embedding_model(model_name):
    if model_name.startswith("hybrid-"):
        return HybridEmbeddingModel(models=[LiteLLMEmbeddingModel(model_name=model_name[7:]), SparseEmbeddingModel(ndim=1024)])
    elif model_name == "sparse":
        return SparseEmbeddingModel(ndim=1024)
    else:
        return LiteLLMEmbeddingModel(model_name=model_name)

def load_user_settings():
    if st.session_state.user_settings:
        return st.session_state.user_settings
    return {}

def save_user_settings(settings):
    st.session_state.user_settings = settings

def save_docs_with_embeddings(docs, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(docs, f)

def load_docs_with_embeddings(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def batch_process_queries(docs, queries, settings):
    results = []
    for query in queries:
        answer = docs.query(query, settings=settings)
        results.append((query, answer.formatted_answer))
    return results