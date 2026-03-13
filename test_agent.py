import requests

BASE_URL = "http://127.0.0.1:8000"

symbol = input("Enter stock symbol: ").upper()

price_url = f"{BASE_URL}/price/{symbol}"
tech_url = f"{BASE_URL}/technical/{symbol}"
news_url = f"{BASE_URL}/news/{symbol}"
strategy_url = f"{BASE_URL}/strategy/{symbol}"

price_response = requests.get(price_url).json()
tech_response = requests.get(tech_url).json()
news_response = requests.get(news_url).json()
strategy_response = requests.get(strategy_url).json()

print("\n===================================")
print(f"STOCK: {symbol}")
print("-----------------------------------")

# -----------------------------
# PRICE DATA
# -----------------------------

if "error" in price_response:
    print("Price Error:", price_response["error"])
else:
    print(f"Price  : ${price_response.get('price')}")
    print(f"Volume : {price_response.get('volume'):,}")

# -----------------------------
# TECHNICAL ANALYSIS
# -----------------------------

print("\nTechnical Analysis")
print("-----------------------------------")

if "error" in tech_response:
    print("Technical Error:", tech_response["error"])
else:
    print(f"RSI    : {tech_response.get('RSI')}")
    print(f"Trend  : {tech_response.get('Moving Average Trend')}")
    print(f"MACD   : {tech_response.get('MACD')}")

# -----------------------------
# NEWS SENTIMENT
# -----------------------------

print("\nNews Sentiment")
print("-----------------------------------")

if "error" in news_response:
    print("News Error:", news_response["error"])
else:
    print(f"Sentiment : {news_response.get('news_sentiment')}")
    print(f"Headline  : {news_response.get('headline')}")

# -----------------------------
# STRATEGY OUTPUT
# -----------------------------

print("\nStrategy Recommendation")
print("-----------------------------------")

if "error" in strategy_response:
    print("Strategy Error:", strategy_response["error"])
else:
    print(f"Recommendation : {strategy_response.get('recommendation')}")
    print(f"Explanation    : {strategy_response.get('explanation')}")

print("===================================\n")