"use client";

import { useState } from "react";
import "./global.css";

export default function Home() {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStock = async () => {
    if (!symbol) return;

    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/strategy/${symbol}`);
      const result = await res.json();
      setData(result);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <header className="header">
        <h1>AI Stock Intelligence</h1>
        <p>Multi-Agent Market Analysis</p>
      </header>

      <div className="searchBox">
        <input
          placeholder="Enter Stock Symbol (AAPL, TSLA...)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        />
        <button onClick={fetchStock}>Analyze</button>
      </div>

      {loading && <div className="loading">Analyzing Market Data...</div>}

      {data && (
        <div className="dashboard">

          <div className="card">
            <h3>Price</h3>
            <p className="value">${data.price}</p>
          </div>

          <div className="card">
            <h3>RSI</h3>
            <p className="value">{data.RSI}</p>
          </div>

          <div className="card">
            <h3>Trend</h3>
            <p className="value">{data.trend}</p>
          </div>

          <div className="card">
            <h3>MACD</h3>
            <p className="value">{data.MACD}</p>
          </div>

          <div className="card">
            <h3>News Sentiment</h3>
            <p className="value">{data.news_sentiment}</p>
          </div>

          <div className="card recommendation">
            <h3>AI Recommendation</h3>
            <p className="signal">{data.recommendation}</p>
            <p className="explanation">{data.explanation}</p>
          </div>

        </div>
      )}

    </div>
  );
}