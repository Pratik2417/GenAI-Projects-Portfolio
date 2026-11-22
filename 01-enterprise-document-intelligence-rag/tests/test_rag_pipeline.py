from langchain.schema import Document
from src.ingestion import chunk_documents

def test_chunk_documents_preserves_metadata():
    docs = [Document(page_content='Enterprise SLA uptime is 99.95% across all regions. ' * 30, metadata={'source': 'sla.pdf', 'page': 2})]
    chunks = chunk_documents(docs)
    assert len(chunks) > 1
    assert all(c.metadata['source'] == 'sla.pdf' and c.metadata['page'] == 2 for c in chunks)
