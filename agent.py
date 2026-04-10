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
    df = df.ffill()  # simple fix
    return df

def analyze_data(df):
    summary = df.describe().round(2).to_string()
    return summary


def create_charts(df):
    figures = []
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax)
        ax.set_title(f"Distribution of {col}")

        figures.append(fig) 

    return figures

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
    summary = df.describe().round(2).to_string()
    columns = ", ".join(df.columns)

    prompt = f"""
    You are a data analyst.

    Dataset columns:
    {columns}

    Statistical summary:
    {summary}

    Question:
    {question}

    Answer clearly based on data.
    """

    return ask_llm(prompt)

def extract_patterns(df):
    insights = ""

    for col in df.select_dtypes(include='number').columns:
        insights += f"{col}: mean={df[col].mean()}, max={df[col].max()}, min={df[col].min()}\n"

    return insights
def suggest_decisions(df):
    patterns = extract_patterns(df)

    prompt = f"""
    You are a business analyst.

    Patterns:
    {patterns}

    Give:
    - 3 business decisions
    - Based on these patterns
    """

    return ask_llm(prompt)