import re
"""Taken from Assignment 1"""
# def tokenize(text):
#     """Returns a list of words that make up the text.

#     Note: for simplicity, lowercase everything.
#     Requirement: Use Regex to satisfy this function

#     Parameters
#     ----------
#     text : str
#         The input string to be tokenized.

#     Returns
#     -------
#     List[str]
#         A list of strings representing the words in the text.
#     """
#     words = re.findall('[a-z]+', text.lower())
#     return words

"""Jaccard function adapted from TA Derek: https://github.com/dliu42/Snack_Surfer/blob/master/backend/helpers/analysis.py"""
# def jaccard(tokens, query):
#     tokens_set = set(tokens)
#     query_set = set(query)
#     return len(tokens_set.intersection(query_set)) / len(tokens_set.union(query_set))

'''
def get_stock_recommendations(query, stock_data):
    """Finds the best matching stocks based on Jaccard similarity.
    
    Parameters
    ----------
    query : str
        The user input query (investment preferences).
    stock_data : dict
        A dictionary where keys are stock symbols and values are stock descriptions.
        This includes risk level, sector, and historical performance.
        
    Returns
    -------
    List[Tuple[str, float]]
        A sorted list of stocks with their similarity scores in descending order.
    """
    query_tokens = tokenize(query)
    
    similarities = []
    for stock, description in stock_data.items():
        description_tokens = tokenize(description)
        similarity_score = jaccard(description_tokens, query_tokens)
        similarities.append((stock, similarity_score))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities'
'''




import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ETFAnalysis:
    def __init__(self, etf_data):
        self.etf_data = etf_data
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', max_features=5000)
        self._prepare_data()
    
    def _prepare_data(self):
        """Creates a textual representation of ETF holdings and sectors for TF-IDF processing."""
        self.etf_corpus = []
        self.etf_labels = []
        
        for etf in self.etf_data:
            description = " ".join([
                etf.get("net_assets", ""),
                etf.get("net_expense_ratio", ""),
                etf.get("portfolio_turnover", ""),
                etf.get("dividend_yield", ""),
                " ".join([s["sector"] for s in etf.get("sectors", [])]),
                " ".join([h["symbol"] + " " + h["description"] for h in etf.get("holdings", [])])
            ])
            
            self.etf_corpus.append(description)
            self.etf_labels.append(etf.get("name", "Unknown ETF"))
        
        self.tfidf_matrix = self.vectorizer.fit_transform(self.etf_corpus)
        self.feature_names = self.vectorizer.get_feature_names_out()
    
    def get_similar_etfs(self, query, top_n=5):
        """Finds ETFs most similar to the given user query using cosine similarity."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[::-1][:top_n]
        
        return [(self.etf_labels[i], similarities[i]) for i in top_indices if similarities[i] > 0]
    
    def get_top_terms(self, n=10):
        """Retrieves the top terms for each ETF based on TF-IDF scores."""
        top_terms = []
        
        for i, label in enumerate(self.etf_labels):
            tfidf_scores = self.tfidf_matrix[i].toarray().flatten()
            sorted_indices = np.argsort(tfidf_scores)[::-1]
            
            document_terms = {self.feature_names[idx]: tfidf_scores[idx] for idx in sorted_indices[:n] if tfidf_scores[idx] > 0}
            top_terms.append({"etf": label, "top_terms": document_terms})
        
        return top_terms