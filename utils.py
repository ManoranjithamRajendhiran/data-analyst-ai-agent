import pandas as pd

def summarize_df(df):
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
        "missing": df.isnull().sum().to_dict()
    }