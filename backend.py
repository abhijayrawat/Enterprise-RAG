import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from modules.data_loader import load_and_split_text
from modules.embed_store import create_vector_store
from modules.retriever import load_vector_store
from modules.chat_engine import build_chat_agent

load_dotenv()

app = FastAPI(title="Domain-Aware Chat API")

# Allow all origins for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat agent
chat_agent = None


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    sources: list


@app.on_event("startup")
async def startup_event():
    """Initialize vector store and chat agent on startup."""
    global chat_agent

    try:
        if not os.path.exists("faiss_index"):
            print("📘 Creating vector store from domain data...")

            if not os.path.exists("data/enterprise_policies.txt"):
                raise FileNotFoundError("data/enterprise_policies.txt not found!")

            docs = load_and_split_text("data/enterprise_policies.txt")
            create_vector_store(docs)
        else:
            print("✅ Using existing FAISS index")

        # Load retriever
        vectorstore = load_vector_store()
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        # Build chat agent
        chat_agent = build_chat_agent(retriever)
        print("🤖 Chat agent ready!")

    except Exception:
        print("❌ Startup failed:")
        traceback.print_exc()


@app.get("/")
async def root():
    return {"message": "Domain-Aware Chat API is running"}


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Process user query and return answer with sources."""
    global chat_agent

    if not chat_agent:
        raise HTTPException(status_code=500, detail="Chat agent not initialized")

    try:
        print(f"🟢 Received query: {request.query}")

        # chat_agent NOW returns answer + sources
        result = chat_agent(request.query)

        print(f"✅ Answer generated: {result['answer'][:100]}...")

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception:
        error_trace = traceback.format_exc()
        print("❌ Exception in /query:\n", error_trace)
        raise HTTPException(status_code=500, detail=error_trace)


@app.post("/rebuild-index")
async def rebuild_index():
    """Rebuild FAISS index from source documents."""
    global chat_agent

    try:
        docs = load_and_split_text("data/enterprise_policies.txt")
        create_vector_store(docs)

        vectorstore = load_vector_store()
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        chat_agent = build_chat_agent(retriever)

        return {"message": "Index rebuilt successfully"}

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Index rebuild failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

