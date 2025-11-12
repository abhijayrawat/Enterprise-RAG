from langchain_community.vectorstores import FAISS
from modules.embed_store import get_hf_embeddings

def load_vector_store(index_path="faiss_index"):
    """Load FAISS index from disk with embeddings."""
    embeddings = get_hf_embeddings()
    return FAISS.load_local(
        index_path, 
        embeddings, 
        allow_dangerous_deserialization=True
    )