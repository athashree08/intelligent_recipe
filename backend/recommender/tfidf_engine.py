from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_recipes(recipes, query):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(recipes + [query])
    return cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()
