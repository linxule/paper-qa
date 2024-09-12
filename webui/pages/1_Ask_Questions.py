import streamlit as st
from paperqa import Settings, ask
from webui.utils import get_embedding_model, load_user_settings, batch_process_queries

st.title("Ask Questions")

user_settings = load_user_settings()

with st.sidebar:
    st.header("Model Settings")
    llm_model = st.selectbox("LLM Model", ["gpt-4o-2024-08-06", "gpt-4o-mini", "claude-3-5-sonnet-20240620"], index=["gpt-4o-2024-08-06", "gpt-4o-mini", "claude-3-5-sonnet-20240620"].index(user_settings.get('llm_model', "gpt-4o-2024-08-06")))
    embedding_model = st.selectbox("Embedding Model", ["text-embedding-3-small", "text-embedding-3-large", "hybrid-text-embedding-3-small", "sparse"], index=["text-embedding-3-small", "text-embedding-3-large", "hybrid-text-embedding-3-small", "sparse"].index(user_settings.get('embedding_model', "text-embedding-3-small")))
    k = st.slider("Number of top passages (k)", 1, 10, user_settings.get('k', 5))
    max_sources = st.slider("Max sources for final answer", 1, 5, user_settings.get('max_sources', 3))
    qa_prompt = st.text_area("QA Prompt", user_settings.get('qa_prompt', "Answer the question '{question}' Use the context below if helpful. You can cite the context using the key like (Example2012).\n\nContext: {context}\n\n"))

query = st.text_input("Enter your question:")

if st.button("Ask"):
    if query:
        with st.spinner("Generating answer..."):
            settings = Settings(
                llm=llm_model,
                embedding=get_embedding_model(embedding_model),
                answer={"k": k, "answer_max_sources": max_sources},
                prompts={"qa": qa_prompt}
            )
            answer = ask(query, settings=settings)
        st.markdown(answer.formatted_answer)
        st.session_state.query_history.append((st.session_state.api_usage['queries'], query, answer.formatted_answer))
        st.session_state.api_usage['queries'] += 1
        st.session_state.api_usage['tokens'] += len(query.split()) + len(answer.formatted_answer.split())

if st.toggle("Enable typewriter output"):
    st.write("Answer:")
    output = st.empty()
    
    def typewriter(chunk: str) -> None:
        output.write(output.text + chunk)
    
    if st.button("Ask (with typewriter)"):
        if query:
            settings = Settings(
                llm=llm_model,
                embedding=get_embedding_model(embedding_model),
                answer={"k": k, "answer_max_sources": max_sources},
                prompts={"qa": qa_prompt}
            )
            answer = ask(query, settings=settings, callbacks=[typewriter])
            st.session_state.query_history.append((st.session_state.api_usage['queries'], query, answer.formatted_answer))
            st.session_state.api_usage['queries'] += 1
            st.session_state.api_usage['tokens'] += len(query.split()) + len(answer.formatted_answer.split())

st.subheader("Batch Processing")
batch_queries = st.text_area("Enter multiple queries (one per line):")
if st.button("Process Batch"):
    if batch_queries:
        queries = batch_queries.split('\n')
        settings = Settings(
            llm=llm_model,
            embedding=get_embedding_model(embedding_model),
            answer={"k": k, "answer_max_sources": max_sources},
            prompts={"qa": qa_prompt}
        )
        with st.spinner("Processing batch queries..."):
            results = batch_process_queries(st.session_state.docs, queries, settings)
        for query, answer in results:
            st.write(f"Q: {query}")
            st.markdown(answer)
            st.write("---")