import streamlit as st
import pandas as pd
import plotly.express as px
from agent import ask_claude
from utils import summarize_df, data_quality_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 AI Data Analyst Pro")
st.caption("Upload CSV • Dashboard • AI Insights • Executive Analytics")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Control Panel")
file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.subheader("💬 Chat History")

if len(st.session_state.history) == 0:
    st.sidebar.info("No questions asked yet")
else:
    for item in st.session_state.history[::-1]:
        st.sidebar.write("Q:", item["question"])

# ---------------- MAIN ----------------
if file:

    df = pd.read_csv(file)

    # ---------------- PREVIEW ----------------
    st.subheader("📁 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ---------------- KPI DASHBOARD ----------------
    summary = summarize_df(df)
    score = data_quality_score(df)

    st.markdown("---")
    st.subheader("📌 KPI Dashboard")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Rows", summary["rows"])
    c2.metric("Columns", summary["columns"])
    c3.metric("Missing", summary["missing"])
    c4.metric("Duplicates", summary["duplicates"])
    c5.metric("Quality Score", f"{score}/100")

    # ---------------- CHART SECTION ----------------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) > 0:

        st.markdown("---")
        st.subheader("📈 Smart Visualization")

        col1, col2 = st.columns(2)

        with col1:
            selected_col = st.selectbox(
                "Choose Numeric Column",
                numeric_cols
            )

        with col2:
            chart_type = st.selectbox(
                "Choose Chart Type",
                ["Histogram", "Box Plot", "Line Chart", "Bar Chart"]
            )

        if chart_type == "Histogram":
            fig = px.histogram(
                df,
                x=selected_col,
                nbins=20,
                title=f"Distribution of {selected_col}"
            )

        elif chart_type == "Box Plot":
            fig = px.box(
                df,
                y=selected_col,
                title=f"Outlier Detection - {selected_col}"
            )

        elif chart_type == "Line Chart":
            fig = px.line(
                df,
                y=selected_col,
                title=f"Trend of {selected_col}"
            )

        else:
            fig = px.bar(
                df.head(20),
                y=selected_col,
                title=f"Top Values of {selected_col}"
            )

        st.plotly_chart(fig, use_container_width=True)

        # -------- GENERATE INSIGHT BUTTON --------
        if st.button("Generate Chart Insight"):

            prompt = f"""
You are a senior business analyst.

Analyze this column:

Column Name: {selected_col}
Mean: {df[selected_col].mean():.2f}
Median: {df[selected_col].median():.2f}
Minimum: {df[selected_col].min():.2f}
Maximum: {df[selected_col].max():.2f}
Std Dev: {df[selected_col].std():.2f}

Give:
1. Distribution Trend
2. Outliers
3. Risk
4. Recommendation
"""

            with st.spinner("Generating insight..."):
                insight = ask_claude(prompt)

            st.subheader("🤖 AI Chart Insight")
            st.success(insight)

    # ---------------- CORRELATION HEATMAP ----------------
    if len(numeric_cols) >= 2:

        st.markdown("---")
        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        heatmap = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Feature Relationship Matrix"
        )

        st.plotly_chart(heatmap, use_container_width=True)

    # ---------------- OUTLIER DETECTOR ----------------
    if len(numeric_cols) > 0:

        st.markdown("---")
        st.subheader("⚠️ Outlier Detector")

        out_col = st.selectbox(
            "Choose Column for Outlier Check",
            numeric_cols,
            key="outlier"
        )

        q1 = df[out_col].quantile(0.25)
        q3 = df[out_col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[
            (df[out_col] < lower) |
            (df[out_col] > upper)
        ]

        st.write("Outlier Count:", len(outliers))

        fig2 = px.box(
            df,
            y=out_col,
            title=f"Outlier Analysis - {out_col}"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- EXECUTIVE SUMMARY ----------------
    st.markdown("---")

    if st.button("Generate Executive Summary"):

        prompt = f"""
You are a senior management consultant.

Dataset Summary:
Rows: {summary['rows']}
Columns: {summary['columns']}
Missing Values: {summary['missing']}
Duplicates: {summary['duplicates']}
Quality Score: {score}/100

Provide:
1. Dataset Health
2. Key Risks
3. Opportunities
4. 3 Executive Recommendations
"""

        with st.spinner("Preparing executive summary..."):
            result = ask_claude(prompt)

        st.subheader("📌 Executive Summary")
        st.success(result)

    # ---------------- ASK DATASET QUESTIONS ----------------
    st.markdown("---")
    st.subheader("💬 Ask Questions About Dataset")

    question = st.text_input("Ask business question")

    if st.button("Analyze Dataset"):

        prompt = f"""
You are a senior business analyst.

Dataset Columns:
{list(df.columns)}

Rows: {summary['rows']}
Columns: {summary['columns']}
Missing Values: {summary['missing']}

Sample Rows:
{df.head(3).to_string()}

Question:
{question}

Respond in format:
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

        st.subheader("📌 AI Response")
        st.success(answer)

else:
    st.info("Upload a CSV file from the sidebar to begin.")