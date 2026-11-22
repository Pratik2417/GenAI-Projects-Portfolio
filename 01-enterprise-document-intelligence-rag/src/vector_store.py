import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.config import settings

class FAISSVectorManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key)
        self.index_path = settings.faiss_index_path
    def build_or_update_index(self, chunks):
        if os.path.exists(self.index_path):
            db = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            db.add_documents(chunks)
        else:
            db = FAISS.from_documents(chunks, self.embeddings)
        os.makedirs(self.index_path, exist_ok=True)
        db.save_local(self.index_path)
        return len(chunks)
    def similarity_search(self, query: str, k: int = settings.top_k):
        if not os.path.exists(self.index_path): return []
        db = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        return [(d, s) for d, s in db.similarity_search_with_relevance_scores(query, k=k) if s >= settings.similarity_threshold]
