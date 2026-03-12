import requests
import pandas as pd
import ta

def analyze_stock(symbol):

    # Call Data Agent API
    url = f"http://127.0.0.1:8000/history/{symbol}"
    response = requests.get(url)

    data = response.json()

    if "history" not in data:
        return {"error": "No data received from Data Agent"}

    df = pd.DataFrame(data["history"])

    # Convert columns
    df["close"] = pd.to_numeric(df["close"])

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()

    # Moving averages
    df["ma50"] = df["close"].rolling(50).mean()
    df["ma200"] = df["close"].rolling(200).mean()

    latest = df.iloc[-1]

    if latest["ma50"] > latest["ma200"]:
        trend = "Uptrend"
    else:
        trend = "Downtrend"

    return {
        "symbol": symbol,
        "RSI": round(latest["rsi"], 2),
        "Moving Average Trend": trend
    }