import streamlit as st
import datetime
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title("Search and Visualize")

st.subheader("Advanced Search")
search_query = st.text_input("Search for papers:")
date_range = st.date_input("Date range", [datetime.date(2020, 1, 1), datetime.date.today()])

if st.button("Search"):
    if search_query:
        results = [doc for doc in st.session_state.docs.docs if search_query.lower() in doc.docname.lower()]
        if results:
            df = pd.DataFrame([
                {
                    "Document Name": doc.docname,
                    "Citation": doc.citation,
                    "Number of Pages": doc.num_pages
                } for doc in results
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
            st.write("No results found.")

st.subheader("Citation Network")
if st.button("Generate Citation Network"):
    G = nx.Graph()
    for doc in st.session_state.docs.docs:
        G.add_node(doc.docname)
        for other_doc in st.session_state.docs.docs:
            if other_doc != doc and np.random.random() < 0.2:  # 20% chance of citation for demonstration
                G.add_edge(doc.docname, other_doc.docname)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=8, font_weight='bold', ax=ax)
    st.pyplot(fig)