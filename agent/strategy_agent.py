import requests
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


class StrategyAgent:

    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

        # Initialize Anthropic client
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    # ----------------------------------
    # FETCH DATA FROM FASTAPI ENDPOINTS
    # ----------------------------------
    def fetch(self, endpoint):

        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            return response.json()

        except Exception as e:
            return {"error": str(e)}

    # ----------------------------------
    # BUILD PORTFOLIO PROMPT FOR AI
    # ----------------------------------
    def build_portfolio_prompt(self, stocks_data):

        return f"""
You are a professional stock portfolio strategist.

Analyze the following stocks and rank them from BEST to WORST investment opportunity.

Stock Data
----------

{stocks_data}

Instructions
------------

1. Rank the stocks from BEST to WORST.
2. Recommend BUY, HOLD, or SELL for each stock.
3. Give one short explanation for each stock.

Respond ONLY in this format:

1. SYMBOL - BUY/HOLD/SELL - explanation
2. SYMBOL - BUY/HOLD/SELL - explanation
3. SYMBOL - BUY/HOLD/SELL - explanation
4. SYMBOL - BUY/HOLD/SELL - explanation

Best Stock: SYMBOL
Reason: one short sentence
"""

    # ----------------------------------
    # COLLECT DATA FOR ONE STOCK
    # ----------------------------------
    def collect_stock_data(self, symbol):

        symbol = symbol.upper()

        price_data = self.fetch(f"/price/{symbol}")
        tech_data = self.fetch(f"/technical/{symbol}")
        news_data = self.fetch(f"/news/{symbol}")

        return {
            "symbol": symbol,
            "price": price_data.get("price"),
            "volume": price_data.get("volume"),
            "RSI": tech_data.get("RSI"),
            "trend": tech_data.get("Moving Average Trend"),
            "MACD": tech_data.get("MACD"),
            "news_sentiment": news_data.get("news_sentiment"),
            "headline": news_data.get("headline")
        }

    # ----------------------------------
    # MAIN PORTFOLIO ANALYSIS
    # ----------------------------------
    def analyze_portfolio(self, symbols):

        symbol_list = [s.strip().upper() for s in symbols.split(",")]

        stocks = []

        # Collect data for each stock
        for sym in symbol_list:
            data = self.collect_stock_data(sym)
            stocks.append(data)

        # Build AI prompt
        prompt = self.build_portfolio_prompt(stocks)

        try:

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = message.content[0].text

        except Exception as e:

            result = f"AI analysis failed: {str(e)}"

        return {
            "stocks": stocks,
            "ai_analysis": result
        }