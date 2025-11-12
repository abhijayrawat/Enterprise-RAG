import streamlit as st
import requests
import json

# Page config
st.set_page_config(
    page_title="Enterprise Policy Assistant",
    page_icon="🤖",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🤖 Enterprise Policy Assistant</p>', unsafe_allow_html=True)
st.markdown("Ask questions about company policies and get instant answers powered by Groq AI!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # System status
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Error")
    except:
        st.error("❌ Backend Not Running")
        st.info("Run: `uvicorn backend:app --reload`")
    
    st.divider()
    
    # Rebuild index button
    if st.button("🔄 Rebuild Index"):
        with st.spinner("Rebuilding index..."):
            try:
                response = requests.post(f"{API_URL}/rebuild-index")
                if response.status_code == 200:
                    st.success("Index rebuilt successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to rebuild: {str(e)}")
    
    st.divider()
    
    st.markdown("### 📚 About")
    st.info("""
    This assistant uses:
    - **Groq API** for fast inference
    - **FAISS** for vector search
    - **LangChain** for RAG pipeline
    - **Streamlit** for UI
    - **FastAPI** for backend
    """)

# Main chat interface
st.header("💬 Ask a Question")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📄 View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {i}:**")
                    st.text(source["content"])

# Chat input
if prompt := st.chat_input("What's the policy for..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"query": prompt}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Display sources
                    if sources:
                        with st.expander("📄 View Sources"):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**Source {i}:**")
                                st.text(source["content"])
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    error_msg = f"Error: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            except Exception as e:
                error_msg = f"Failed to get response: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()