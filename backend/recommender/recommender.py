from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(recipes, user_ingredients):
    documents = [" ".join(r["ingredients"]) for r in recipes]
    query = " ".join(user_ingredients)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(documents + [query])

    scores = cosine_similarity(tfidf[-1], tfidf[:-1])[0]

    for i, score in enumerate(scores):
        recipes[i]["similarity"] = round(float(score), 3)

    return sorted(recipes, key=lambda x: x["similarity"], reverse=True)
