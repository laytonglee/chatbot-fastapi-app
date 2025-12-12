import os
import re
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer, CrossEncoder
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download("punkt")
nltk.download("wordnet")

# Paths
model_path = os.path.join(os.path.dirname(__file__), "models/pipeline_svm.joblib")
faq_path   = os.path.join(os.path.dirname(__file__), "models/faq_with_embeddings.joblib")

# Load models and data
pipeline = joblib.load(model_path)
df_faq = joblib.load(faq_path)
sbert = SentenceTransformer("all-MiniLM-L6-v2")  
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_text(text: str) -> str:
    """Clean and lemmatize text."""
    text = str(text).lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

def hybrid_chatbot(query: str, top_k: int = 5) -> dict:
    """
    Returns the best FAQ match using:
    1. SVM category prediction
    2. SBERT cosine similarity
    3. Cross-Encoder reranking (top-K)
    """
    query_clean = clean_text(query)

    # STEP 1 — Predict category
    pred_category = pipeline.predict([query_clean])[0]
    df_cat = df_faq[df_faq["category"] == pred_category]

    if df_cat.empty:
        return {
            "category": None,
            "answer": "No matching FAQ found in this category.",
            "similarity": 0.0
        }

    # STEP 2 — SBERT embedding and cosine similarity
    query_emb = sbert.encode(query_clean)
    embeddings = np.vstack(df_cat["embedding"].values)
    cosine_sim = embeddings @ query_emb / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb)
    )

    # STEP 3 — Top-K selection
    top_k_idx = np.argsort(cosine_sim)[-top_k:][::-1]
    top_k_rows = df_cat.iloc[top_k_idx]

    # STEP 4 — Cross-Encoder reranking
    pairs = [(query_clean, row["question"]) for _, row in top_k_rows.iterrows()]
    cross_scores = cross_encoder.predict(pairs)
    best_idx = np.argmax(cross_scores)
    faq_row = top_k_rows.iloc[best_idx]

    final_similarity = float(cosine_sim[top_k_idx[best_idx]])

    return {
        "category": faq_row["category"],
        "answer": faq_row["answer"],
        "similarity": final_similarity
    }
