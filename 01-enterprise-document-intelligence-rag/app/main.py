import os, shutil, tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from src.ingestion import extract_pdf_documents, chunk_documents
from src.vector_store import FAISSVectorManager
from src.rag_chain import EnterpriseRAGService

app = FastAPI(title='Enterprise Document Intelligence RAG API')
vm, rag = FAISSVectorManager(), EnterpriseRAGService()

class QueryRequest(BaseModel):
    question: str

@app.post('/ingest')
async def ingest(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'): raise HTTPException(400, 'PDF only')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name
    try:
        docs = extract_pdf_documents(path)
        for d in docs: d.metadata['source'] = file.filename
        return {'filename': file.filename, 'chunks_indexed': vm.build_or_update_index(chunk_documents(docs))}
    finally:
        os.remove(path)

@app.post('/query')
def query(req: QueryRequest):
    return rag.answer_query(req.question)
