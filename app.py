import streamlit as st
import pandas as pd
import plotly.express as px
from agent import ask_claude
from utils import summarize_df

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("📊 AI Data Analyst Pro")
st.caption("Upload CSV • Smart Charts • AI Insights • Business Recommendations")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # ---------------- TOP SECTION ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📁 Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

    with col2:
        st.subheader("📌 Quick Stats")
        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    # ---------------- CHART SECTION ----------------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) >= 1:

        st.markdown("---")
        st.subheader("📈 Smart Visualization")

        selected_col = st.selectbox(
            "Choose Numeric Column",
            numeric_cols
        )

        chart_type = st.selectbox(
            "Choose Chart Type",
            ["Histogram", "Box Plot", "Line Chart", "Bar Chart"]
        )

        if chart_type == "Histogram":
            chart = px.histogram(
                df,
                x=selected_col,
                nbins=20,
                title=f"Distribution of {selected_col}"
            )

        elif chart_type == "Box Plot":
            chart = px.box(
                df,
                y=selected_col,
                title=f"Outlier Detection - {selected_col}"
            )

        elif chart_type == "Line Chart":
            chart = px.line(
                df,
                y=selected_col,
                title=f"Trend of {selected_col}"
            )

        else:
            chart = px.bar(
                df.head(20),
                y=selected_col,
                title=f"Top Values of {selected_col}"
            )

        st.plotly_chart(chart, use_container_width=True)

        # -------- BUTTON TO GENERATE INSIGHT --------
        if st.button("Generate Chart Insight"):

            chart_prompt = f"""
You are a senior business analyst.

Analyze this column:

Column Name: {selected_col}
Mean: {df[selected_col].mean():.2f}
Median: {df[selected_col].median():.2f}
Minimum: {df[selected_col].min():.2f}
Maximum: {df[selected_col].max():.2f}
Standard Deviation: {df[selected_col].std():.2f}

Give:
1. Distribution Trend
2. Outliers / unusual values
3. Risk
4. Recommendation
"""

            with st.spinner("Generating insight..."):
                chart_insight = ask_claude(chart_prompt)

            st.subheader("🤖 AI Chart Insight")
            st.info(chart_insight)

    # ---------------- QUESTION SECTION ----------------
    st.markdown("---")
    st.subheader("💬 Ask Questions About Dataset")

    question = st.text_input("Ask your business question")

    if st.button("Analyze Dataset"):

        summary = summarize_df(df)

        prompt = f"""
You are a senior business analyst.

Dataset Summary:
Rows: {summary['rows']}
Columns: {summary['columns']}
Missing Values: {summary['missing']}

Sample Rows:
{df.head(3).to_string()}

Question:
{question}

Respond in this format:
1. Direct Answer
2. Key Insight
3. Recommendation
4. Risk
"""

        with st.spinner("Claude is analyzing..."):
            answer = ask_claude(prompt)

        st.session_state.history.append(
            {"question": question, "answer": answer}
        )

        st.subheader("📌 Claude Analysis")
        st.success(answer)

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 Chat History")

if len(st.session_state.history) == 0:
    st.sidebar.info("No history yet")
else:
    for item in st.session_state.history[::-1]:
        st.sidebar.write("**Q:**", item["question"])