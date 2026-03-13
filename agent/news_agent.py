import feedparser
from textblob import TextBlob


def get_news_sentiment(symbol: str):

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