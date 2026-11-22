import fitz
from langchain_openai import ChatOpenAI
from src.schemas import ResumeMatchReport

def extract_pdf_text(data: bytes) -> str:
    with fitz.open(stream=data, filetype='pdf') as doc:
        return '\n'.join(p.get_text('text') for p in doc).strip()

class ResumeJDAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.0).with_structured_output(ResumeMatchReport)
    def evaluate(self, resume_text: str, jd: str) -> ResumeMatchReport:
        return self.llm.invoke(f'Compare resume to JD.\nJD:\n{jd}\n\nResume:\n{resume_text}')
