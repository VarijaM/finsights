import os
import json
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from helpers.analysis import get_top_etf_matches, extract_etf_text

app = Flask(__name__)
CORS(app)

# Load all ETF JSON files from the 'etfs' folder
etf_directory = os.path.join(os.path.dirname(__file__), "etfs")
etf_files = [f for f in os.listdir(etf_directory) if f.endswith(".json")]

etf_list = []
for etf_file in etf_files:
    file_path = os.path.join(etf_directory, etf_file)
    with open(file_path, "r") as file:
        data = json.load(file)
        # Assuming each file contains a single ETF object (adjust if it's a list)
        if isinstance(data, list):
            for etf in data:
                # Optionally, add a 'name' field if missing using the filename
                if 'name' not in etf:
                    etf['name'] = etf_file.split('.')[0]
                etf_list.append(etf)
        else:
            if 'name' not in data:
                data['name'] = etf_file.split('.')[0]
            etf_list.append(data)

@app.route("/")
def home():
    return "FinSights Stock Recommendation API"

@app.route("/stocks", methods=["GET"])
def stock_search():
    user_query = request.args.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Get the top ETF matches based on the query
    top_matches = get_top_etf_matches(user_query, etf_list, top_n=5)

    # Format the response to include ETF name, a snippet of its combined description, and the score.
    results = []
    for etf, score in top_matches:
        result = {
            "name": etf.get("name", "Unknown"),
            "description": extract_etf_text(etf)[:250] + "..." if len(extract_etf_text(etf)) > 250 else extract_etf_text(etf),
            "similarity_score": score
        }
        results.append(result)
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)