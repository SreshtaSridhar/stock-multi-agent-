from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import ta
import os
from dotenv import load_dotenv
import feedparser
from textblob import TextBlob

# Load environment variables
load_dotenv()

# Read values from .env
HISTORY_PERIOD = os.getenv("DEFAULT_HISTORY_PERIOD", "6mo")
PRICE_PERIOD = os.getenv("DEFAULT_PRICE_PERIOD", "1d")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Stock Data Agent Running"}


# -----------------------------
# DATA AGENT
# -----------------------------

# Fetch current stock price
@app.get("/price/{symbol}")
def get_stock_price(symbol: str):

    stock = yf.Ticker(symbol)
    data = stock.history(period=PRICE_PERIOD)

    if data.empty:
        return {"error": "Invalid stock symbol"}

    latest = data.iloc[-1]

    return {
        "symbol": symbol.upper(),
        "price": round(latest["Close"], 2),
        "volume": int(latest["Volume"])
    }


# Fetch historical OHLC data
@app.get("/history/{symbol}")
def get_stock_history(symbol: str):

    stock = yf.Ticker(symbol)
    data = stock.history(period=HISTORY_PERIOD)

    if data.empty:
        return {"error": "Invalid stock symbol"}

    history = []

    for index, row in data.iterrows():
        history.append({
            "date": str(index.date()),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"])
        })

    return {
        "symbol": symbol.upper(),
        "history": history
    }


# -----------------------------
# TECHNICAL ANALYSIS AGENT
# -----------------------------

@app.get("/technical/{symbol}")
def technical_analysis(symbol: str):

    stock = yf.Ticker(symbol)
    data = stock.history(period=HISTORY_PERIOD)

    if data.empty:
        return {"error": "Invalid stock symbol"}

    df = data.copy()

    # RSI
    rsi_indicator = ta.momentum.RSIIndicator(df["Close"])
    df["RSI"] = rsi_indicator.rsi()

    # Moving Averages
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    # MACD
    macd_indicator = ta.trend.MACD(df["Close"])
    df["MACD"] = macd_indicator.macd()
    df["MACD_SIGNAL"] = macd_indicator.macd_signal()

    latest = df.iloc[-1]

    # Moving average trend
    if latest["MA50"] > latest["MA200"]:
        trend = "Uptrend"
    else:
        trend = "Downtrend"

    # MACD signal
    if latest["MACD"] > latest["MACD_SIGNAL"]:
        macd_signal = "Bullish crossover"
    else:
        macd_signal = "Bearish crossover"

    return {
        "symbol": symbol.upper(),
        "RSI": round(latest["RSI"], 2),
        "Moving Average Trend": trend,
        "MACD": macd_signal
    }


# -----------------------------
# NEWS & SENTIMENT AGENT
# -----------------------------

@app.get("/news/{symbol}")
def news_sentiment(symbol: str):

    url = f"https://news.google.com/rss/search?q={symbol}+stock"

    feed = feedparser.parse(url)

    if len(feed.entries) == 0:
        return {"error": "No news found"}

    headline = feed.entries[0].title

    analysis = TextBlob(headline)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "symbol": symbol.upper(),
        "headline": headline,
        "news_sentiment": sentiment
    }