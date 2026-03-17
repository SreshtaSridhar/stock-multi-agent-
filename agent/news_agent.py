import feedparser
from textblob import TextBlob


def get_news_sentiment(symbol: str):

    url = f"https://news.google.com/rss/search?q={symbol}+stock"

    feed = feedparser.parse(url)

    if len(feed.entries) == 0:
        return {"error": "No news found"}

    # headline = feed.entries[0].title

    # analysis = TextBlob(headline)
    # polarity = analysis.sentiment.polarity

    headlines = [entry.title for entry in feed.entries[:5]]

    if not headlines:
        return {"error": "No news found"}

    total_polarity = 0

    for h in headlines:
        analysis = TextBlob(h)
        total_polarity += analysis.sentiment.polarity

    avg_polarity = total_polarity / len(headlines)

    if avg_polarity > 0:
        sentiment = "Positive"
    elif avg_polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "symbol": symbol.upper(),
        "headline": headlines[0],
        "news_sentiment": sentiment
    }

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