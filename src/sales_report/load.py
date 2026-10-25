import pandas as pd


def load_sales(path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    for name, col in df.iteritems():
        if col.dtype == object:
            df[name] = col.str.strip()
    return df
