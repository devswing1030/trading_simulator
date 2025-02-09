import React, { useState, useEffect } from 'react';

const StockScreen= () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from the backend API
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch('/nasdaq/topn'); // Replace with your API endpoint
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const result = await response.json();
      setData(result.data);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  // Fetch data initially and set up the periodic refresh
  useEffect(() => {
    fetchData(); // Initial fetch

    const intervalId = setInterval(() => {
      fetchData(); // Periodic fetch every 5 seconds (5000 ms)
    }, 5000);

    // Cleanup: Clear the interval when the component is unmounted
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array means this effect runs only once when the component mounts

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Nasdaq Top 10 Valued Company Screen</h1>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Company Name</th>
            <th>Last Sale</th>
            <th>Bid</th>
            <th>Ask</th>
            <th>Volume</th>
            <th>ClosePx</th>
            <th>Market</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {data.map((post) => (
            <tr key={post.symbol}>
              <td>{post.symbol}</td>
              <td>{post.name}</td>
              <td>{post.last_px}</td>
              <td>{post.bid_px=='' ? '' : post.bid_px + ' X ' + post.bid_qty}</td>
              <td>{post.ask_px=='' ? '' : post.ask_px + ' X ' + post.ask_qty}</td>
              <td>{post.volume}</td>
              <td>{post.close_px}</td>
              <td>{post.market_status}</td>
              <td>{post.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StockScreen;