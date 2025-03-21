# import os
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from helpers.analysis import get_top_etf_matches, extract_etf_text

# app = Flask(__name__)
# CORS(app)

# # Load all ETF JSON files from the 'etfs' folder.
# etf_directory = os.path.join(os.path.dirname(__file__), "etfs")
# etf_files = [f for f in os.listdir(etf_directory) if f.endswith(".json")]

# etf_list = []
# for etf_file in etf_files:
#     file_path = os.path.join(etf_directory, etf_file)
#     with open(file_path, "r") as file:
#         data = json.load(file)
#         # Handle both single ETF objects or lists of ETFs.
#         if isinstance(data, list):
#             for etf in data:
#                 if 'name' not in etf:
#                     etf['name'] = etf_file.split('.')[0]
#                 etf_list.append(etf)
#         else:
#             if 'name' not in data:
#                 data['name'] = etf_file.split('.')[0]
#             etf_list.append(data)

# @app.route("/")
# def home():
#     return "FinSights Stock Recommendation API"

# @app.route("/stocks", methods=["GET"])
# def stock_search():
#     user_query = request.args.get("query", "")
#     if not user_query:
#         return jsonify({"error": "No query provided"}), 400

#     # Debug print to verify query and number of ETFs loaded.
#     print(f"Received query: {user_query}")
#     print(f"Number of ETFs loaded: {len(etf_list)}")

#     # Get the top ETF matches based on the query.
#     top_matches = get_top_etf_matches(user_query, etf_list, top_n=5)

#     # Format the response to include ETF name, a snippet of its combined description, and the score.
#     results = []
#     for etf, score in top_matches:
#         full_text = extract_etf_text(etf)
#         result = {
#             "name": etf.get("name", "Unknown"),
#             "description": full_text[:250] + "..." if len(full_text) > 250 else full_text,
#             "similarity_score": score
#         }
#         results.append(result)
    
#     # Debug: print results to console.
#     print("Top matches:", results)
    
#     return jsonify(results)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)






# their code starts here


# import json
# import os
# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
# import pandas as pd

# # ROOT_PATH for linking with all your files. 
# # Feel free to use a config.py or settings.py with a global export variable
# os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# # Get the directory of the current script
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Specify the path to the JSON file relative to the current script
# json_file_path = os.path.join(current_directory, 'init.json')

# # Assuming your JSON data is stored in a file named 'init.json'
# with open(json_file_path, 'r') as file:
#     data = json.load(file)

# animals_df = pd.DataFrame(data)
# print(animals_df.head())

# if 'id' not in animals_df.columns or 'full_description' not in animals_df.columns:
#     raise ValueError("Expected 'id' and 'full_description' fields in JSON data")

# app = Flask(__name__)
# CORS(app)

# # Sample search using json with pandas
# def json_search(query):
#     query = query.lower()
#     matches = animals_df[animals_df['full_description'].str.lower().str.contains(query, na=False)]
#     matches['image_url'] = matches['photos'].apply(lambda x: x[0]['small'] if isinstance(x, list) and x else "https://via.placeholder.com/300")
#     matches_filtered = matches[['id', 'name', 'url', 'type', 'species', 'age', 'gender', 'status', 'image_url','full_description']]
#     return matches_filtered.to_json(orient='records')


# @app.route("/")
# def home():
#     return render_template('base.html', title="Sample HTML")

# @app.route("/animals")
# def animals_search():
#     text = request.args.get("query")
#     if not text:
#         return jsonify({"error": "Query parameter is required"}), 400
#     return json_search(text)

# if 'DB_NAME' not in os.environ:
#     app.run(debug=True,host="0.0.0.0",port=5000)


import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd

# Set ROOT_PATH for linking with all files
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the JSON file relative to the current script
json_file_path = os.path.join(current_directory, 'init.json')

# Load investment data from JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

investments_df = pd.DataFrame(data)
print(investments_df.head())

# Ensure required fields exist
required_columns = {'id', 'name', 'type', 'sector', 'risk_level', 'amount', 'reasoning'}
if not required_columns.issubset(investments_df.columns):
    raise ValueError(f"Missing expected fields in JSON data: {required_columns - set(investments_df.columns)}")

app = Flask(__name__)
CORS(app)

# Function to filter investments based on user query
def search_investments(sector, risk_appetite, amount):
    filtered_df = investments_df

    if sector:
        filtered_df = filtered_df[filtered_df['sector'].str.lower().str.contains(sector.lower(), na=False)]
    
    if risk_appetite:
        filtered_df = filtered_df[filtered_df['risk_level'].str.lower() == risk_appetite.lower()]

    if amount:
        amount = float(amount)
        filtered_df = filtered_df[filtered_df['amount'] <= amount]

    return filtered_df[['id', 'name', 'type', 'sector', 'risk_level', 'amount', 'reasoning']].to_json(orient='records')

@app.route("/")
def home():
    return render_template('base.html', title="FinSights")

@app.route("/investments")
def investments_search():
    sector = request.args.get("sectors")
    risk_appetite = request.args.get("risk_appetite")
    amount = request.args.get("amount")

    if not (sector and risk_appetite and amount):
        return jsonify({"error": "All query parameters (sectors, risk_appetite, amount) are required"}), 400

    return search_investments(sector, risk_appetite, amount)

if 'DB_NAME' not in os.environ:
    app.run(debug=True, host="0.0.0.0", port=5000)
