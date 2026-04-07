import pandas as pd
import matplotlib.pyplot as plt
from utils import ask_llm
def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.read_excel(file)

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(method='ffill')  # simple fix
    return df

def analyze_data(df):
    summary = df.describe(include='all').to_string()
    return summary


def create_charts(df):
    charts = []

    for col in df.select_dtypes(include='number').columns:
        plt.figure()
        df[col].hist()
        filename = f"{col}.png"
        plt.savefig(filename)
        charts.append(filename)
        plt.close()

    return charts

def get_insights(summary):
    prompt = f"""
    You are a professional data analyst.

    Give:
    - key insights
    - Trends
    - Anomaly

    Data:
    {summary}
    """

    return ask_llm(prompt)

def ask_question(df, question):
    sample = df.head().to_string()

    prompt = f"""
    You are a data analyst.

    Dataset sample:
    {sample}

    Answer this question:
    {question}
    """

    return ask_llm(prompt)

def suggest_decisions(summary):
    prompt = f"""
    Based on this data, suggest business decisions:

    {summary}
    """
    return ask_llm(prompt)