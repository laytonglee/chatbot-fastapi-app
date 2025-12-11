import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
import os

model_path = os.path.join(os.path.dirname(__file__), "models/pipeline_svm.joblib")
faq_path   = os.path.join(os.path.dirname(__file__), "models/faq_with_embeddings.joblib")

pipeline = joblib.load(model_path)
df_faq = joblib.load(faq_path)


sbert = SentenceTransformer("all-MiniLM-L6-v2")


def hybrid_chatbot(query: str):
    """
    Returns the best FAQ match based on category prediction + cosine similarity
    """
    # Predict category with SVM
    pred_category = pipeline.predict([query])[0]

    # Filter FAQs by predicted category
    df_cat = df_faq[df_faq["category"] == pred_category]

    # Encode query with SBERT
    query_emb = sbert.encode(query)

    # Stack embeddings of FAQs
    embeddings = np.vstack(df_cat["embedding"].values)

    # Cosine similarity
    cosine_sim = embeddings @ query_emb / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb)
    )

    # Get the index of the best match
    idx = np.argmax(cosine_sim)
    faq_row = df_cat.iloc[idx]

    return {
        "category": faq_row["category"],
        "answer": faq_row["answer"],
        "similarity": float(cosine_sim[idx])
    }
