import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Plot from 'react-plotly.js';


function App() {
  const [formData, setFormData] = useState({
    S0: '',
    K: '',
    T: '',
    r: '',
    sigma: '',
    option_type: 'call'
  });

  const [plotData, setPlotData] = useState(null);
  
  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const res = await axios.post('http://localhost:8000/plot', formData);
    setPlotData(JSON.parse(res.data.plot_json));
  };

  return (
    <div className="container">
      <div className="form-section">
        <h1>Black-Scholes Calculator</h1>
        <form onSubmit={handleSubmit} className="form-grid">
          <div>
            <input type="number" name="S0" placeholder="Stock Price (S₀)" onChange={handleChange} required />
            <input type="number" name="T" placeholder="Maturity (T)" onChange={handleChange} required />
            <input type="number" name="sigma" placeholder="Volatility (σ)" step="0.01" onChange={handleChange} required />
          </div>
          <div>
            <input type="number" name="K" placeholder="Strike Price (K)" onChange={handleChange} required />
            <input type="number" name="r" placeholder="Risk-Free Rate (r)" step="0.01" onChange={handleChange} required />
            <select name="option_type" onChange={handleChange}>
              <option value="call">Call Option</option>
              <option value="put">Put Option</option>
            </select>
          </div>
          <button type="submit">Generate Plot</button>
        </form>
      </div>

      <div className="plot-section">
        {plotData && (
          <Plot
            data={plotData.data}
            layout={plotData.layout}
            config={{ responsive: true }}
          />
        )}
      </div>
    </div>
  );
}

export default App;
