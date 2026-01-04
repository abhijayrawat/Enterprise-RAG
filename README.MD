# Enterprise-RAG: Domain-Aware Chat Assistant

A Python-based Retrieval-Augmented Generation (RAG) system designed for querying enterprise documents. This application allows users to ask questions about company policies and receive accurate, context-aware answers powered by AI.

## Architecture Overview

This application uses a Retrieval-Augmented Generation (RAG) approach:

1. **Document Processing**: Enterprise policies are loaded and split into smaller chunks
2. **Vector Embeddings**: Text chunks are converted to numerical vectors using Google Gemini embeddings
3. **Vector Storage**: Embeddings are stored in FAISS (Facebook AI Similarity Search) for fast retrieval
4. **Query Processing**: When a user asks a question, the system finds the most relevant document chunks
5. **Answer Generation**: The retrieved chunks are sent to Groq's LLM along with the question to generate a coherent answer

This ensures answers are based on your actual enterprise documents rather than general knowledge.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI |
| Frontend Framework | Streamlit |
| Vector Database | FAISS |
| LLM Provider | Groq API |
| Embeddings | Google Gemini |
| Text Processing | LangChain |
| Programming Language | Python 3.8+ |

## Folder Structure

```
Enterprise-RAG/
├── backend.py              # FastAPI backend server
├── streamlit_app.py        # Streamlit frontend interface
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env                   # Environment variables (create this)
├── data/
│   └── enterprise_policies.txt  # Your enterprise documents
├── faiss_index/
│   └── index.faiss        # Vector database (auto-generated)
└── modules/
    ├── __init__.py
    ├── chat_engine.py     # LLM integration
    ├── data_loader.py     # Document processing
    ├── embed_store.py     # Vector storage
    └── retriever.py       # Document retrieval
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher installed
- Git (optional, for cloning)

### Step-by-Step Setup

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd Enterprise-RAG
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Your Documents**
   - Place your enterprise documents in the `data/` folder
   - The system expects a file named `enterprise_policies.txt`
   - Format: Plain text with clear section headers

4. **Set Up Environment Variables**
   - Copy the example environment file: `cp .env.example .env` (if provided)
   - Or create a new `.env` file in the root directory
   - Add your API keys (see Environment Variables section below)

## Virtual Environment Setup

It's recommended to use a virtual environment to isolate project dependencies.

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To deactivate the virtual environment later:
```bash
deactivate
```

## Environment Variables (.env) Explanation

Create a `.env` file in the project root with the following variables:

```env
# Required: Your Groq API key for LLM inference
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

# Optional: Specify which Groq model to use (default: llama-3.3-70b-versatile)
GROQ_MODEL=llama-3.3-70b-versatile

# Required: Your Google API key for Gemini embeddings
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

**Important**: 
- Never commit your `.env` file to version control
- Get API keys from:
  - [Groq Console](https://console.groq.com/)
  - [Google AI Studio](https://makersuite.google.com/app/apikey)

## Running the Application

### Start the Backend (FastAPI)
```bash
uvicorn backend:app --reload
```
The backend will start on `http://localhost:8000`

### Start the Frontend (Streamlit)
Open a new terminal and run:
```bash
streamlit run streamlit_app.py
```
The frontend will open in your browser at `http://localhost:8501`

### Alternative: Run Both Together
On Windows PowerShell:
```powershell
start "Backend" uvicorn backend:app --reload
start "Frontend" streamlit run streamlit_app.py
```

## Rebuilding the Vector Index

The vector index is automatically created on first run. To rebuild it after updating documents:

### Via API
```bash
curl -X POST http://localhost:8000/rebuild-index
```

### Via Streamlit Interface
1. Open the Streamlit app
2. Click the "🔄 Rebuild Index" button in the sidebar
3. Wait for the success message

This is useful when you add new documents or modify existing ones.

## Example Usage / Sample Questions

Once running, try asking questions like:

- "What is the remote work policy?"
- "How do I report a data breach?"
- "What are the access control requirements?"
- "Can customer data be shared externally?"
- "What should I do if I suspect a security incident?"

The system will provide answers based on your enterprise policies with relevant source citations.

## Common Errors & Troubleshooting

### NumPy Compatibility Issues
**Error**: `numpy.core.multiarray failed to import`
**Solution**: Upgrade NumPy and ensure compatible versions:
```bash
pip install --upgrade numpy
pip install --upgrade faiss-cpu
```

### FAISS Installation Problems
**Error**: `No module named 'faiss'`
**Solution**: 
- On Windows: `pip install faiss-cpu`
- On macOS/Linux: `pip install faiss-cpu` or `conda install faiss-cpu -c pytorch`

### Environment Variable Issues
**Error**: `KeyError: 'GROQ_API_KEY'`
**Solution**: 
- Ensure `.env` file exists in project root
- Check variable names match exactly (case-sensitive)
- Restart the application after adding variables

### Backend Connection Failed
**Error**: "Backend Not Running" in Streamlit
**Solution**: 
- Ensure backend is started: `uvicorn backend:app --reload`
- Check if port 8000 is available
- Verify no firewall blocking localhost connections

### Document Loading Errors
**Error**: `FileNotFoundError: data/enterprise_policies.txt`
**Solution**: 
- Ensure the file exists in the `data/` folder
- Check file permissions
- Verify the file is not empty

## Security Best Practices

- **API Keys**: Never commit `.env` files to version control. Use `.gitignore`
- **Access Control**: Limit who can access the application in production
- **Data Privacy**: Ensure enterprise documents don't contain sensitive information
- **Network Security**: Use HTTPS in production and restrict CORS origins
- **Logging**: Monitor API usage and implement rate limiting
- **Updates**: Keep dependencies updated and monitor for security vulnerabilities

## Future Improvements / Roadmap

- Support for multiple document formats (PDF, DOCX, etc.)
- Multi-language support for international enterprises
- Advanced search with filters and metadata
- User authentication and role-based access
- Integration with enterprise document management systems
- Batch processing for large document collections
- Performance optimization for high-traffic deployments
- UI enhancements with better source visualization

## License & Contribution Guidelines

This project is licensed under the MIT License. See LICENSE file for details.

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

### Support
For issues or questions:
- Check the troubleshooting section above
- Open an issue on GitHub
- Ensure you've followed all setup steps

---

**Note**: This is an enterprise-grade application. For production deployment, consider containerization with Docker and proper security hardening.