"use client";

import { useState } from "react";

export default function Home() {

  const [symbols, setSymbols] = useState("");
  const [stocks, setStocks] = useState([]);
  const [ranking, setRanking] = useState([]);

  const fetchStocks = async () => {

    if (!symbols) return;

    const list = symbols.split(",").map(s => s.trim().toUpperCase());

    let results = [];

    for (let symbol of list) {

      const res = await fetch(`http://127.0.0.1:8000/strategy/${symbol}`);
      const data = await res.json();

      console.log(data); // DEBUG

      results.push(data);
    }

    setStocks(results);

    // ranking based on RSI
    const sorted = [...results].sort((a, b) => b.RSI - a.RSI);

    setRanking(sorted);
  };

  return (

    <div className="container">

      <h1>AI Stock Portfolio Analyzer</h1>

      <div className="inputBox">

        <input
          type="text"
          placeholder="Enter stocks (AAPL,TSLA,AMZN,GOOG)"
          value={symbols}
          onChange={(e) => setSymbols(e.target.value)}
        />

        <button onClick={fetchStocks}>Analyze</button>

      </div>


      {/* STOCK TABLE */}

      {stocks.length > 0 && (

        <table>

          <thead>
            <tr>
              <th>Symbol</th>
              <th>Price</th>
              <th>Volume</th>
              <th>RSI</th>
              <th>Trend</th>
              <th>MACD</th>
              <th>Sentiment</th>
              <th>Recommendation</th>
              <th>Explanation</th>
            </tr>
          </thead>

          <tbody>

            {stocks.map((s, i) => (

              <tr key={i}>

                <td>{s.symbol}</td>

                <td>${s.price}</td>

                <td>{s.volume?.toLocaleString()}</td>

                <td>{s.RSI}</td>

                <td>{s.trend}</td>

                <td>{s.MACD}</td>

                <td>{s.news_sentiment}</td>

                <td className="rec">{s.recommendation}</td>

                <td>{s.explanation}</td>

              </tr>

            ))}

          </tbody>

        </table>

      )}


      {/* HEADLINES */}

      {stocks.length > 0 && (

        <div className="news">

          <h2>Latest Headlines</h2>

          {stocks.map((s, i) => (

            <p key={i}>
              <b>{s.symbol}</b> → {s.headline}
            </p>

          ))}

        </div>

      )}


      {/* PORTFOLIO RANKING */}

      {ranking.length > 0 && (

        <div className="ranking">

          <h2>Portfolio Ranking (Based on RSI)</h2>

          {ranking.map((s, index) => (

            <p key={index}>

              {index + 1}. {s.symbol}

            </p>

          ))}

        </div>

      )}

    </div>
  );
}