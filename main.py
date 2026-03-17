from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import ta
import os
from dotenv import load_dotenv
import feedparser
from textblob import TextBlob
from openai import OpenAI

load_dotenv()

HISTORY_PERIOD = os.getenv("DEFAULT_HISTORY_PERIOD", "1y")
PRICE_PERIOD = os.getenv("DEFAULT_PRICE_PERIOD", "1d")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Stock Multi-Agent System Running"}


# -----------------------------
# PRICE AGENT
# -----------------------------
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


# -----------------------------
# TECHNICAL AGENT
# -----------------------------
@app.get("/technical/{symbol}")
def technical_analysis(symbol: str):

    stock = yf.Ticker(symbol)
    data = stock.history(period=HISTORY_PERIOD)

    if data.empty:
        return {"error": "Invalid stock symbol"}

    df = data.copy()

    rsi_indicator = ta.momentum.RSIIndicator(df["Close"])
    df["RSI"] = rsi_indicator.rsi()

    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    macd_indicator = ta.trend.MACD(df["Close"])
    df["MACD"] = macd_indicator.macd()
    df["MACD_SIGNAL"] = macd_indicator.macd_signal()

    latest = df.iloc[-1]

    trend = "Uptrend" if latest["MA50"] > latest["MA200"] else "Downtrend"

    macd_signal = (
        "Bullish crossover"
        if latest["MACD"] > latest["MACD_SIGNAL"]
        else "Bearish crossover"
    )

    return {
        "symbol": symbol.upper(),
        "RSI": round(latest["RSI"], 2),
        "Moving Average Trend": trend,
        "MACD": macd_signal
    }


# -----------------------------
# NEWS AGENT
# -----------------------------
@app.get("/news/{symbol}")
def news_sentiment(symbol: str):

    try:

        url = f"https://news.google.com/rss/search?q={symbol}+stock"
        feed = feedparser.parse(url)

        if len(feed.entries) == 0:
            return {
                "symbol": symbol.upper(),
                "headline": "No recent news found",
                "news_sentiment": "Neutral"
            }

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

    except Exception:

        return {
            "symbol": symbol.upper(),
            "headline": "News unavailable",
            "news_sentiment": "Neutral"
        }


# -----------------------------
# STRATEGY AGENT
# -----------------------------
@app.get("/strategy/{symbol}")
def strategy(symbol: str):

    price_data = get_stock_price(symbol)
    tech_data = technical_analysis(symbol)
    news_data = news_sentiment(symbol)

    if "error" in price_data:
        return price_data

    prompt = f"""
You are a professional stock market analyst.

Analyze the following stock data.

Stock: {symbol}

Price: {price_data['price']}
Volume: {price_data['volume']}

RSI: {tech_data['RSI']}
Trend: {tech_data['Moving Average Trend']}
MACD: {tech_data['MACD']}

News Sentiment: {news_data['news_sentiment']}
Headline: {news_data['headline']}

Respond exactly in this format:

Recommendation: BUY/HOLD/SELL
Explanation: one short sentence
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        recommendation = "HOLD"
        explanation = ""

        for line in result.split("\n"):
            if "Recommendation" in line:
                recommendation = line.split(":")[1].strip()
            if "Explanation" in line:
                explanation = line.split(":")[1].strip()

    except Exception:

        trend = tech_data["Moving Average Trend"]
        macd = tech_data["MACD"]
        sentiment = news_data["news_sentiment"]

        # if trend == "Uptrend" and macd == "Bullish crossover" and sentiment == "Positive":
        #     recommendation = "BUY"
        #     explanation = "Strong bullish signals."
        # elif trend == "Downtrend" and macd == "Bearish crossover" and sentiment == "Negative":
        #     recommendation = "SELL"
        #     explanation = "Strong bearish signals."
        # else:
        #     recommendation = "HOLD"
        #     explanation = "Mixed market signals."

        score = 0

    # Trend
    if trend == "Uptrend":
        score += 2

    # MACD
    if macd == "Bullish crossover":
        score += 2
    elif macd == "Bearish crossover":
        score -= 2

    # RSI
    if tech_data["RSI"] > 60:
        score += 1
    elif tech_data["RSI"] < 40:
        score -= 1

    # Sentiment
    if sentiment == "Positive":
        score += 1
    elif sentiment == "Negative":
        score -= 1

    # Final decision
    if score >= 3:
        recommendation = "BUY"
        explanation = "Multiple bullish signals."
    elif score <= -2:
        recommendation = "SELL"
        explanation = "Multiple bearish signals."
    else:
        recommendation = "HOLD"
        explanation = "Mixed signals."

    return {

        "symbol": symbol.upper(),

        "price": price_data["price"],
        "volume": price_data["volume"],

        "RSI": tech_data["RSI"],
        "trend": tech_data["Moving Average Trend"],
        "MACD": tech_data["MACD"],

        "news_sentiment": news_data["news_sentiment"],
        "headline": news_data["headline"],

        "recommendation": recommendation,
        "explanation": explanation

    }