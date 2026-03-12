from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stock Data Agent Running"}

# Fetch current stock price
@app.get("/price/{symbol}")
def get_stock_price(symbol: str):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")

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
    data = stock.history(period="5d")

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