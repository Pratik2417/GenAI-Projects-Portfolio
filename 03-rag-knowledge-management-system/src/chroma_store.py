from typing import Optional
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class KnowledgeBaseVectorStore:
    def __init__(self, persist_dir: str = './data/chroma_kb'):
        emb = HuggingFaceEmbeddings(model_name='BAAI/bge-small-en-v1.5', encode_kwargs={'normalize_embeddings': True})
        self.db = Chroma(collection_name='enterprise_kb', embedding_function=emb, persist_directory=persist_dir)
    def ingest_article(self, title: str, content: str, department: str) -> int:
        chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120).split_documents([Document(page_content=content, metadata={'title': title, 'department': department.lower()})])
        self.db.add_documents(chunks)
        return len(chunks)
    def search_mmr(self, query: str, department: Optional[str] = None):
        kw = {'k': 4, 'fetch_k': 12}
        if department: kw['filter'] = {'department': department.lower()}
        return self.db.as_retriever(search_type='mmr', search_kwargs=kw).invoke(query)
