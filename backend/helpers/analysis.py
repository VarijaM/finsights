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