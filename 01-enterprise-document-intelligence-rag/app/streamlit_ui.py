import requests, streamlit as st
API = 'http://localhost:8001'
st.title('Enterprise Document Intelligence - RAG Assistant')
f = st.file_uploader('Upload PDF', type=['pdf'])
if f and st.button('Index'):
    st.json(requests.post(f'{API}/ingest', files={'file': (f.name, f.getvalue(), 'application/pdf')}).json())
q = st.text_input('Ask a question:')
if st.button('Ask') and q:
    st.json(requests.post(f'{API}/query', json={'question': q}).json())
