from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from src.chroma_store import KnowledgeBaseVectorStore

app = FastAPI(title='RAG Knowledge Management System')
store = KnowledgeBaseVectorStore()
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.0)

class Article(BaseModel):
    title: str
    content: str
    department: str

class Query(BaseModel):
    question: str
    department: Optional[str] = None

@app.post('/kb/articles')
def add_article(a: Article):
    return {'chunks': store.ingest_article(a.title, a.content, a.department)}

@app.post('/kb/ask')
def ask(q: Query):
    docs = store.search_mmr(q.question, q.department)
    ctx = '\n\n'.join(d.page_content for d in docs)
    ans = llm.invoke(f'Answer from context:\n{ctx}\n\nQuestion: {q.question}').content
    return {'answer': ans, 'sources': list({d.metadata['title'] for d in docs})}
