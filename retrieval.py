"""
retrieval.py
------------
Simple, dependency-light retrieval layer for the RAG pipeline.

Uses TF-IDF + cosine similarity (scikit-learn) rather than a heavy vector
database or embedding API. This is a deliberate choice for a 2-day student
project: it needs no API key, no external service, and no GPU, and it
retrieves correctly for a knowledge base of this size. For a production
system you'd swap this for sentence-embeddings + a vector store (e.g.
FAISS + a sentence-transformers model), but the RAG *pattern* - retrieve
relevant context, then ground generation in it - is identical either way.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import KNOWLEDGE_BASE


class Retriever:
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base or KNOWLEDGE_BASE
        self.documents = [f"{d['topic']}. {d['content']}" for d in self.kb]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 2, min_score: float = 0.05):
        """
        Returns the top_k most relevant KB entries for a query, each with
        a similarity score. Entries below min_score are dropped - this
        prevents the system from confidently answering questions it has
        no real knowledge base coverage for (an important RAG safeguard).
        """
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.doc_vectors)[0]

        ranked = sorted(
            zip(self.kb, scores), key=lambda pair: pair[1], reverse=True
        )

        results = [
            {**entry, "score": round(float(score), 3)}
            for entry, score in ranked[:top_k]
            if score >= min_score
        ]
        return results


if __name__ == "__main__":
    r = Retriever()
    test_queries = [
        "how do I throw away my old phone battery",
        "can I compost eggshells",
        "my water pressure is low",  # should retrieve poorly / nothing relevant
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = r.retrieve(q)
        if not results:
            print("  No confident match in knowledge base.")
        for res in results:
            print(f"  [{res['score']}] {res['topic']} -> {res['content'][:80]}...")
