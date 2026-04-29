import pandas as pd

def summarize_df(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }

def data_quality_score(df):
    rows, cols = df.shape
    total = rows * cols if rows * cols > 0 else 1

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    penalty = (missing / total) * 50 + (duplicates / rows) * 50
    score = max(0, round(100 - penalty))

    return score