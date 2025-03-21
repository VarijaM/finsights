# import re
# import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def tokenize(text):
#     """
#     Returns a list of words (tokens) from the text using regex.
#     Lowercases everything for simplicity.
#     """
#     words = re.findall('[a-z]+', text.lower())
#     return words

# def jaccard(tokens, query_tokens):
#     """
#     Computes the Jaccard similarity between two sets of tokens.
    
#     Parameters:
#         tokens (List[str]): Tokens from a text.
#         query_tokens (List[str]): Tokens from the query.
        
#     Returns:
#         float: Jaccard similarity score.
#     """
#     tokens_set = set(tokens)
#     query_set = set(query_tokens)
#     union = tokens_set.union(query_set)
#     if not union:
#         return 0.0
#     return len(tokens_set.intersection(query_set)) / len(union)

# def cosine_sim(text1, text2):
#     """
#     Computes the cosine similarity between two texts using CountVectorizer.
    
#     Parameters:
#         text1 (str): First text.
#         text2 (str): Second text.
        
#     Returns:
#         float: Cosine similarity score.
#     """
#     vectorizer = CountVectorizer()
#     vectors = vectorizer.fit_transform([text1, text2])
#     cos_sim_matrix = cosine_similarity(vectors)
#     return cos_sim_matrix[0, 1]

# def extract_etf_text(etf, filename=None):
#     """
#     Extracts a consolidated text description from an ETF's data.
#     Combines available fields such as ETF name, description, sectors, and holdings.
    
#     Parameters:
#         etf (dict): ETF data.
#         filename (str, optional): The filename from which the ETF was loaded (used if 'name' is missing).
    
#     Returns:
#         str: Combined textual description.
#     """
#     text_parts = []
#     # Use ETF 'name' if available, otherwise derive it from the filename.
#     if 'name' in etf:
#         text_parts.append(etf['name'])
#     elif filename:
#         text_parts.append(filename.split('.')[0])
    
#     if 'description' in etf:
#         text_parts.append(etf['description'])
        
#     # Process sectors if available.
#     if 'sectors' in etf and isinstance(etf['sectors'], list):
#         sector_names = " ".join([s.get('sector', '') for s in etf['sectors']])
#         text_parts.append(sector_names)
    
#     # Process holdings if available: combine the descriptions of holdings.
#     if 'holdings' in etf and isinstance(etf['holdings'], list):
#         holdings_text = " ".join([h.get('description', '') for h in etf['holdings']])
#         text_parts.append(holdings_text)
    
#     return " ".join(text_parts)

# def compute_similarity_score(query, etf_text):
#     """
#     Computes a combined similarity score between the query and an ETF's combined text.
#     Uses a weighted sum of Jaccard similarity and cosine similarity.
    
#     Parameters:
#         query (str): The user's query.
#         etf_text (str): Combined ETF text.
    
#     Returns:
#         float: Similarity score.
#     """
#     query_tokens = tokenize(query)
#     etf_tokens = tokenize(etf_text)
#     jac_score = jaccard(etf_tokens, query_tokens)
#     cos_score = cosine_sim(query, etf_text)
#     # For now, equal weights (these can be tuned further)
#     score = 0.5 * jac_score + 0.5 * cos_score
#     return score

# def get_top_etf_matches(query, etf_list, top_n=5):
#     """
#     Given a query and a list of ETFs (each represented as a dict),
#     computes similarity scores and returns the top N matching ETFs.
    
#     Additionally, if the query indicates technology, it will filter for known technology ETFs.
    
#     Parameters:
#         query (str): The user's search query.
#         etf_list (List[dict]): List of ETF data dictionaries.
#         top_n (int): Number of top matches to return.
    
#     Returns:
#         List[tuple]: Each tuple contains (etf, similarity_score).
#     """
#     # Fallback: if query mentions "tech" or "technology", return known technology ETFs.
#     tech_tickers = {"VGT", "XLK", "SMH", "IYW"}
#     if "tech" in query.lower() or "technology" in query.lower():
#         tech_matches = [etf for etf in etf_list if etf.get("name", "").upper() in tech_tickers]
#         if tech_matches:
#             # Return them with a dummy high score so they appear at the top.
#             return [(etf, 1.0) for etf in tech_matches][:top_n]
    
#     # Otherwise, perform the standard similarity matching.
#     scores = []
#     for etf in etf_list:
#         etf_text = extract_etf_text(etf)
#         score = compute_similarity_score(query, etf_text)
#         scores.append(score)
    
#     top_indices = np.argsort(scores)[::-1][:top_n]
#     top_matches = [(etf_list[i], scores[i]) for i in top_indices]
#     return top_matches
