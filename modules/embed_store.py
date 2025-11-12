from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def get_hf_embeddings():
    """Use a free local embedding model."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(documents, index_path="faiss_index"):
    """Embed documents and store in FAISS using HuggingFace."""
    embeddings = get_hf_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(index_path)
    print(f"✅ FAISS index saved at {index_path}/")
    return vectorstore
