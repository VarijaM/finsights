import re
"""Taken from Assignment 1"""
def tokenize(text):
    """Returns a list of words that make up the text.

    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function

    Parameters
    ----------
    text : str
        The input string to be tokenized.

    Returns
    -------
    List[str]
        A list of strings representing the words in the text.
    """
    words = re.findall('[a-z]+', text.lower())
    return words

"""Jaccard function adapted from TA Derek: https://github.com/dliu42/Snack_Surfer/blob/master/backend/helpers/analysis.py"""
def jaccard(tokens, query):
    tokens_set = set(tokens)
    query_set = set(query)
    return len(tokens_set.intersection(query_set)) / len(tokens_set.union(query_set))

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