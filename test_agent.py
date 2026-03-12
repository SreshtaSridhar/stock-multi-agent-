import requests

symbol = input("Enter stock symbol: ").upper()

price_url = f"http://127.0.0.1:8000/price/{symbol}"
tech_url = f"http://127.0.0.1:8000/technical/{symbol}"
news_url = f"http://127.0.0.1:8000/news/{symbol}"

price_response = requests.get(price_url).json()
tech_response = requests.get(tech_url).json()
news_response = requests.get(news_url).json()

print("\n===================================")
print(f"STOCK: {symbol}")
print("-----------------------------------")

# Price Data
print(f"Price  : ${price_response['price']}")
print(f"Volume : {price_response['volume']:,}")

print("\nTechnical Analysis")
print("-----------------------------------")

# Technical Data
print(f"RSI    : {tech_response['RSI']}")
print(f"Trend  : {tech_response['Moving Average Trend']}")
print(f"MACD   : {tech_response['MACD']}")

print("\nNews Sentiment")
print("-----------------------------------")

# News Data
print(f"Sentiment : {news_response['news_sentiment']}")
print(f"Headline  : {news_response['headline']}")

print("===================================\n")