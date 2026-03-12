import yfinance as yf
import pandas as pd


class StockDataAgent:

    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_current_price(self):
        stock = yf.Ticker(self.symbol)
        data = stock.history(period="1d")

        if data.empty:
            return {"error": "No data found"}

        latest = data.iloc[-1]

        return {
            "symbol": self.symbol,
            "price": float(latest["Close"]),
            "volume": int(latest["Volume"])
        }

    def get_historical_data(self, period="1mo"):
        stock = yf.Ticker(self.symbol)
        hist = stock.history(period=period)

        if hist.empty:
            return {"error": "No historical data"}

        hist.reset_index(inplace=True)

        records = []

        for _, row in hist.iterrows():
            records.append({
                "date": str(row["Date"]),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })

        return {
            "symbol": self.symbol,
            "historical_data": records
        }