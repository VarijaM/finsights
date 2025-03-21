import os
import json
import pandas as pd
import re
from collections import defaultdict

# Path to ETF data (modify if needed)
ETF_DATA_PATH = os.path.join(os.path.dirname(__file__), "backend/etfs")

# ETF Sector Mapping
ETF_SECTOR_DATA = {
    "QQQ": "Technology", "VGT": "Technology", "XLK": "Technology", "SMH": "Technology", "IYW": "Technology",
    "XLV": "Healthcare", "VHT": "Healthcare", "IBB": "Healthcare", "XBI": "Healthcare", "IHI": "Healthcare",
    "XLE": "Energy", "AMLP": "Energy", "VDE": "Energy", "JNK": "Energy",
    "XLF": "Finance", "VFH": "Finance", "MINT": "Finance", "BOND": "Finance", "NVDL": "Finance",
    "XLY": "Consumer Goods", "VCR": "Consumer Goods", "TSLL": "Consumer Goods", "ITB": "Consumer Goods", "FDIS": "Consumer Goods"
}

# Hardcoded ETF prices (Replace with API fetching later)
PRICE_DATA = {
    "QQQ": 370, "VGT": 430, "XLK": 180, "SMH": 160, "IYW": 90,
    "XLV": 140, "VHT": 240, "IBB": 125, "XBI": 85, "IHI": 55,
    "XLE": 85, "AMLP": 35, "VDE": 110, "JNK": 95,
    "XLF": 40, "VFH": 90, "MINT": 100, "BOND": 85, "NVDL": 55,
    "XLY": 175, "VCR": 190, "TSLL": 80, "ITB": 75, "FDIS": 60
}

def load_etf_data():
    """Loads ETF holdings from JSON files in backend/etfs."""
    etf_holdings = defaultdict(list)

    for filename in os.listdir(ETF_DATA_PATH):
        if filename.endswith(".json"):
            with open(os.path.join(ETF_DATA_PATH, filename), "r") as file:
                data = json.load(file)
                etf_name = data.get("name", filename.replace(".json", ""))
                
                for holding in data.get("holdings", []):
                    etf_holdings[etf_name].append({
                        "symbol": holding["symbol"],
                        "weight": float(holding["weight"])
                    })

    return etf_holdings

def filter_etfs_by_risk(risk_appetite):
    """Returns ETFs based on user risk appetite."""
    return list(ETF_SECTOR_DATA.keys()) if risk_appetite.lower() in ["low", "medium"] else []

def get_sector_recommendations(etfs, preferred_sectors):
    """Filters ETFs by user sector preferences."""
    matched_etfs = [etf for etf in etfs if ETF_SECTOR_DATA.get(etf) in preferred_sectors]
    return matched_etfs if matched_etfs else etfs  # Default to all ETFs if no sector match

def calculate_etf_allocation(total_investment, etfs):
    """Allocates investment evenly across selected ETFs."""
    num_assets = len(etfs)
    allocation_per_etf = total_investment / num_assets

    investment_breakdown = {}
    for etf in etfs:
        price = PRICE_DATA.get(etf, 100)  # Default price if missing
        num_shares = round(allocation_per_etf / price, 2)
        investment_breakdown[etf] = {"investment": round(allocation_per_etf, 2), "shares": num_shares}

    return investment_breakdown

def get_top_stocks(etf_holdings, num_stocks=5):
    """Finds the top weighted stocks from all ETFs."""
    stock_weights = defaultdict(float)

    for etf, holdings in etf_holdings.items():
        for stock in holdings:
            stock_weights[stock["symbol"]] += stock["weight"]

    # Sort stocks by total weight across all ETFs
    sorted_stocks = sorted(stock_weights.items(), key=lambda x: x[1], reverse=True)

    return sorted_stocks[:num_stocks]

def generate_investment_summary(risk, sectors, investment_amount, breakdown):
    """Generates a summary of ETF investment recommendations."""
    output = f"\n**Investment Summary**\n"
    output += f"Risk Appetite: {risk}\n"
    output += f"Preferred Sectors: {', '.join(sectors)}\n"
    output += f"Total Investment: ${investment_amount}\n\n"
    
    output += "**Recommended ETFs:**\n"
    for etf, details in breakdown.items():
        output += f"- {etf}: Invest ${details['investment']}, Approx. {details['shares']} shares\n"
    
    output += "\n**Explanation:**\n"
    if risk.lower() == "low":
        output += "Since you prefer low risk, diversified ETFs were chosen to minimize volatility.\n"
    elif risk.lower() == "medium":
        output += "Your balanced approach led to a selection of sector-focused ETFs.\n"

    return output

def tokenize(text):
    """Tokenizes input text into lowercase words using regex."""
    words = re.findall('[a-z]+', text.lower())
    return words

def jaccard(tokens, query):
    """Computes Jaccard similarity between two sets of tokens."""
    tokens_set = set(tokens)
    query_set = set(query)
    return len(tokens_set.intersection(query_set)) / len(tokens_set.union(query_set))