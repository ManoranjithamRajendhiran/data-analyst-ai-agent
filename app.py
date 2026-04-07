import streamlit as st
from agent import load_data, analyze_data, get_insights, ask_question

st.title("📊 AI Data Analyst Agent")

file = st.file_uploader("Upload your dataset")

if file:
    df = load_data(file)

    st.write("### Data Preview")
    st.write(df.head())

    if st.button("Analyze Data"):
        summary = analyze_data(df)
        insights = get_insights(summary)

        st.write("### Insights")
        st.write(insights)

    question = st.text_input("Ask a question about your data")

    if question:
        answer = ask_question(df, question)
        st.write("### Answer")
        st.write(answer)