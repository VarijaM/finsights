import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from helpers.analysis import (
    filter_etfs_by_risk,
    get_sector_recommendations,
    calculate_etf_allocation,
    load_etf_data,
    get_top_stocks,
    tokenize,
    jaccard
)

app = Flask(__name__)
CORS(app)

# Load ETF holdings (once at startup)
etf_holdings = load_etf_data()

@app.route("/")
def home():
    """Render the frontend page."""
    return render_template('index.html')

@app.route("/investments", methods=["GET"])
def get_investment_recommendations():
    """Handles user input and returns investment recommendations."""
    
    # Extract user input
    sectors = request.args.get("sectors", "").split(",") if request.args.get("sectors") else []
    risk_appetite = request.args.get("risk_appetite", "Medium")
    investment_amount = float(request.args.get("amount", 1000))
    investment_horizon = request.args.get("horizon", "Long-term")

    # Ensure some default sectors if none are provided
    if not sectors:
        sectors = ["Technology", "Healthcare", "Finance"]

    # Step 1: Filter ETFs by risk level
    etfs = filter_etfs_by_risk(risk_appetite)

    # Step 2: Filter ETFs by sector preferences
    sector_filtered_etfs = get_sector_recommendations(etfs, sectors)

    # Step 3: Allocate investment
    investment_breakdown = calculate_etf_allocation(investment_amount, sector_filtered_etfs)

    # Step 4: Format the response for the frontend
    investments = []
    for etf, details in investment_breakdown.items():
        investments.append({
            "name": etf,
            "type": "ETF",
            "sector": ", ".join(sectors),
            "amount": details["investment"],
            "reasoning": f"{etf} is a well-diversified ETF that aligns with your sector preference."
        })

    return jsonify(investments)

@app.route("/top-stocks", methods=["GET"])
def get_top_etf_stocks():
    """Returns the top stocks weighted in ETFs."""
    num_stocks = int(request.args.get("num", 5))  # Default to top 5 stocks
    top_stocks = get_top_stocks(etf_holdings, num_stocks)

    return jsonify([
        {"symbol": stock, "weight": f"{weight:.2f}%"} for stock, weight in top_stocks
    ])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)