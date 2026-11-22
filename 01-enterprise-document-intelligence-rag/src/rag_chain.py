from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import settings
from src.vector_store import FAISSVectorManager

PROMPT = 'Answer strictly from the context and cite [Source, Page].\nContext:\n{context}'

class EnterpriseRAGService:
    def __init__(self):
        self.vm = FAISSVectorManager()
        self.llm = ChatOpenAI(model=settings.llm_model, temperature=0.0, api_key=settings.openai_api_key)
        self.prompt = ChatPromptTemplate.from_messages([('system', PROMPT), ('human', '{question}')])
    def answer_query(self, question: str):
        matches = self.vm.similarity_search(question)
        if not matches: return {'answer': 'Insufficient evidence in indexed documents.', 'citations': [], 'confidence': 0.0}
        ctx, cites = [], []
        for doc, score in matches:
            src, pg = doc.metadata.get('source'), doc.metadata.get('page')
            ctx.append(f'\n{doc.page_content}')
            cites.append({'source': src, 'page': pg, 'score': round(float(score), 4)})
        res = (self.prompt | self.llm).invoke({'context': '\n\n'.join(ctx), 'question': question})
        return {'answer': res.content, 'citations': cites, 'confidence': round(sum(c['score'] for c in cites)/len(cites), 4)}
