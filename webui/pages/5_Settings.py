import streamlit as st
from webui.utils import load_user_settings, save_user_settings

st.title("Settings")

user_settings = load_user_settings()

llm_model = st.selectbox("Default LLM Model", ["gpt-4o-2024-08-06", "gpt-4o-mini", "claude-3-5-sonnet-20240620"], index=["gpt-4o-2024-08-06", "gpt-4o-mini", "claude-3-5-sonnet-20240620"].index(user_settings.get('llm_model', "gpt-4o-2024-08-06")))
embedding_model = st.selectbox("Default Embedding Model", ["text-embedding-3-small", "text-embedding-3-large", "hybrid-text-embedding-3-small", "sparse"], index=["text-embedding-3-small", "text-embedding-3-large", "hybrid-text-embedding-3-small", "sparse"].index(user_settings.get('embedding_model', "text-embedding-3-small")))
k = st.slider("Default Number of top passages (k)", 1, 10, user_settings.get('k', 5))
max_sources = st.slider("Default Max sources for final answer", 1, 5, user_settings.get('max_sources', 3))
qa_prompt = st.text_area("Default QA Prompt", user_settings.get('qa_prompt', "Answer the question '{question}' Use the context below if helpful. You can cite the context using the key like (Example2012).\n\nContext: {context}\n\n"))

if st.button("Save Settings"):
    new_settings = {
        'llm_model': llm_model,
        'embedding_model': embedding_model,
        'k': k,
        'max_sources': max_sources,
        'qa_prompt': qa_prompt
    }
    save_user_settings(new_settings)
    st.success("Settings saved successfully!")