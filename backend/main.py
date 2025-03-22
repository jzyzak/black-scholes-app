from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scipy.stats import norm
import numpy as np
import plotly.graph_objects as go

app = FastAPI()

# Allow requests from frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptionRequest(BaseModel):
    S0: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: str

def black_scholes(S0, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    return price

@app.post("/calculate") # POST request to /calculate
def calculate(data: OptionRequest):
    price = black_scholes(data.S0, data.K, data.T, data.r, data.sigma, data.option_type)
    return {"price": round(price,2)}

@app.post("/plot") # POST request to /plot
def plot(data: OptionRequest):
    sigmas = np.linspace(0.05, 1.0, 50)
    prices = [black_scholes(data.S0, data.K, data.T, data.r, sigma, data.option_type) for sigma in sigmas]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sigmas, y=prices, mode='lines+markers'))
    fig.update_layout(
        template="plotly_dark",
        title="Option Price vs Volatility",
        xaxis_title="Volatility (σ)",
        yaxis_title="Option Price",
        height=600
    )
    
    return {"plot_json": fig.to_json()}