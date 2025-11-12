from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

def load_and_split_text(file_path: str, chunk_size=200, overlap=50):
    """Load and split domain text into chunks."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = CharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=overlap,
        separator="\n"
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]