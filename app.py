import streamlit as st
from agent import *

st.set_page_config(layout="wide")
st.title("📊 AI Data Analyst Agent")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

file = st.file_uploader("Upload CSV or Excel")

if file:
    df = load_data(file)
    df = clean_data(df)

    # Filters
    column = st.sidebar.selectbox("Select Column", df.columns)

    if df[column].dtype == 'object':
        value = st.sidebar.selectbox("Value", df[column].unique())
        df = df[df[column] == value]

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧠 Insights", "💬 Ask"])

    with tab1:
        st.subheader("📌 Overview")
        show_kpis(df)

        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        st.subheader("📈 Charts")

        charts = create_charts(df)

        col1, col2 = st.columns(2)

        for i, chart in enumerate(charts):
            if i % 2 == 0:
                col1.image(chart)
            else:
                col2.image(chart)

    with tab2:
        st.subheader("🧠 AI Insights")

        summary = analyze_data(df)

        if st.button("Generate Insights"):
            insights = generate_insights(summary)
            st.success(insights)

        st.subheader("💡 Decision Suggestions")

        if st.button("Suggest Decisions"):
            decisions = suggest_decisions(summary)
            st.info(decisions)

    with tab3:
        st.subheader("💬 Ask Questions")

        question = st.text_input("Enter your question")

        if question:
            answer = ask_question(df, question)
            st.write(answer)

else:
    st.info("👆 Upload a dataset to start")