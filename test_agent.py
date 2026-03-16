import requests

BASE_URL = "http://127.0.0.1:8000"

symbols_input = input("Enter stock symbols (comma separated): ").upper()
symbols = [s.strip() for s in symbols_input.split(",")]

stocks_data = []

for symbol in symbols:

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

    score = 0

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
        rsi = tech_response.get("RSI")
        trend = tech_response.get("Moving Average Trend")
        macd = tech_response.get("MACD")

        print(f"RSI    : {rsi}")
        print(f"Trend  : {trend}")
        print(f"MACD   : {macd}")

        if trend == "Uptrend":
            score += 2

        if macd == "Bullish crossover":
            score += 2

        if rsi and rsi > 60:
            score += 1

    # -----------------------------
    # NEWS SENTIMENT
    # -----------------------------

    print("\nNews Sentiment")
    print("-----------------------------------")

    if "error" in news_response:
        print("News Error:", news_response["error"])
    else:
        sentiment = news_response.get("news_sentiment")
        headline = news_response.get("headline")

        print(f"Sentiment : {sentiment}")
        print(f"Headline  : {headline}")

        if sentiment == "Positive":
            score += 1

    # -----------------------------
    # STRATEGY OUTPUT
    # -----------------------------

    print("\nStrategy Recommendation")
    print("-----------------------------------")

    if "error" in strategy_response:
        print("Strategy Error:", strategy_response["error"])
        recommendation = "HOLD"
        explanation = ""
    else:
        recommendation = strategy_response.get("recommendation")
        explanation = strategy_response.get("explanation")

        print(f"Recommendation : {recommendation}")
        print(f"Explanation    : {explanation}")

    print("===================================\n")

    stocks_data.append({
        "symbol": symbol,
        "score": score,
        "recommendation": recommendation
    })

# -----------------------------
# PORTFOLIO COMPARISON
# -----------------------------

stocks_sorted = sorted(stocks_data, key=lambda x: x["score"], reverse=True)

print("\nPORTFOLIO COMPARISON")
print("===================================")

best_stock = stocks_sorted[0]["symbol"]

print(f"\nBest Stock → {best_stock}")

print("\nRanking")
print("-----------------------------------")

rank = 1
for stock in stocks_sorted:
    print(f"{rank}️⃣ {stock['symbol']}  (Score: {stock['score']})")
    rank += 1

print("\n===================================\n")