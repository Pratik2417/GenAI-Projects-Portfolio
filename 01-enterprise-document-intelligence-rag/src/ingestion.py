from pathlib import Path
import fitz
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import settings

def extract_pdf_documents(file_path: str):
    path = Path(file_path)
    docs = []
    with fitz.open(path) as pdf:
        for i, page in enumerate(pdf, start=1):
            txt = ' '.join(page.get_text('text').split())
            if txt:
                docs.append(Document(page_content=txt, metadata={'source': path.name, 'page': i}))
    return docs

def chunk_documents(documents):
    return RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap).split_documents(documents)
