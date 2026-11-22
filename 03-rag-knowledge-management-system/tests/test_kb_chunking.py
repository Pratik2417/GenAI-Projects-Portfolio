from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def test_kb_metadata_preservation():
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_documents([Document(page_content='Kubernetes rollout policy. ' * 20, metadata={'department': 'engineering'})])
    assert len(chunks) > 1 and all(c.metadata['department'] == 'engineering' for c in chunks)
