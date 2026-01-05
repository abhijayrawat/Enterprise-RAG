import os
from langchain_groq import ChatGroq

def build_chat_agent(retriever):
    """Build RAG chat agent that returns answer + sources"""

    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0.3,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    def query(question: str):
        # Retrieve documents from FAISS
        retrieved_docs = retriever.invoke(question)

        # Build context for LLM
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        prompt = f"""
You are a helpful assistant for enterprise policy questions.
Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

        response = llm.invoke(prompt)

        # Return BOTH answer and sources
        return {
            "answer": response.content,
            "sources": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in retrieved_docs
            ]
        }

    return query
