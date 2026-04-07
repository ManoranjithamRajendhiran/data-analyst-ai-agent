import pandas as pd
from utils import ask_llm
def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.read_excel(file)


def analyze_data(df):
    summary = df.describe(include='all').to_string()
    sample=df.head(5).to_string()

    return f"""
    SUMMARY:
    {summary}

    MISSING VALUES
    {sample}
    """


def get_insights(summary):
    prompt = f"""
    You are a professional data analyst.

    Give:
    1. 3 key insights
    2. 2 trends
    3. 1 anomaly (if any)

    Keep answer short and clear.

    Data:
    {summary}
    """

    return ask_llm(prompt)

def ask_question(df, question):
    sample = df.head(5).to_string()

    prompt = f"""
    You are a data analyst.

    Dataset sample:
    {sample}

    Answer this question:
    {question}
    """

    return ask_llm(prompt)