import pandas as pd

def load_valid_tickers():
    df = pd.read_csv("tickers.csv")
    return set(df['symbol'].astype(str).str.upper())

def is_valid_ticker(ticker, valid_tickers):
    return ticker.upper() in valid_tickers
