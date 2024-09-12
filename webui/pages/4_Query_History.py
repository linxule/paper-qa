import streamlit as st
import pandas as pd

st.title("Query History")

if st.session_state.query_history:
    df = pd.DataFrame(st.session_state.query_history, columns=['Query ID', 'Question', 'Answer'])
    st.dataframe(
        df,
        column_config={
            "Query ID": st.column_config.NumberColumn("Query ID", format="%d"),
            "Question": st.column_config.TextColumn("Question", width="medium"),
            "Answer": st.column_config.TextColumn("Answer", width="large"),
        },
        hide_index=True,
    )

    if st.button("Export Query History"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="query_history.csv",
            mime="text/csv",
        )
else:
    st.write("No queries have been made yet.")