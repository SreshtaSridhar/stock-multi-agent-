import requests
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

class StrategyAgent:

    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def fetch(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def build_prompt(self, price_data, tech_data, news_data):

        return f"""
You are a professional stock market analyst.

Analyze the following data and recommend whether to BUY, HOLD, or SELL the stock.

Stock Data
-----------
Price : {price_data.get('price')}
Volume : {price_data.get('volume')}

Technical Indicators
-------------------
RSI : {tech_data.get('RSI')}
Trend : {tech_data.get('Moving Average Trend')}
MACD : {tech_data.get('MACD')}

News Sentiment
--------------
Sentiment : {news_data.get('news_sentiment')}
Headline : {news_data.get('headline')}

Respond ONLY in this format:

Recommendation: BUY/HOLD/SELL
Explanation: one short sentence
"""

    def analyze(self, symbol):

        symbol = symbol.upper()

        price_data = self.fetch(f"/price/{symbol}")
        tech_data = self.fetch(f"/technical/{symbol}")
        news_data = self.fetch(f"/news/{symbol}")

        prompt = self.build_prompt(price_data, tech_data, news_data)

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=150,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = message.content[0].text

        recommendation = "HOLD"
        explanation = ""

        for line in result.split("\n"):
            if "Recommendation" in line:
                recommendation = line.split(":")[1].strip()
            if "Explanation" in line:
                explanation = line.split(":")[1].strip()

        return {
            "symbol": symbol,
            "recommendation": recommendation,
            "explanation": explanation
        }