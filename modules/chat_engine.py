import os
from langchain_groq import ChatGroq

def build_chat_agent(retriever):
    """Build a lightweight RAG-style Groq chat agent without LangChain chains."""
    
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0.3,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    def query(question: str):
        # ✅ New API for LCEL retrievers
        retrieved_docs = retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        prompt = f"""You are a helpful assistant for enterprise policy questions.
Use the context below to answer the question accurately and concisely.
If the context does not contain enough information, say you don't know.

Context:
{context}

Question:
{question}

Answer:"""

        response = llm.invoke(prompt)
        return response.content  # ChatGroq returns an object with `.content`
    
    return query
    