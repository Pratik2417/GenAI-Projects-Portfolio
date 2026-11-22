from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from src.analyzer import ResumeJDAnalyzer, extract_pdf_text
from src.schemas import ResumeMatchReport

app = FastAPI(title='AI Resume Analyzer & JD Matcher API')
analyzer = ResumeJDAnalyzer()

class TextReq(BaseModel):
    resume_text: str
    job_description: str

@app.post('/analyze/text', response_model=ResumeMatchReport)
def analyze_text(req: TextReq):
    return analyzer.evaluate(req.resume_text, req.job_description)

@app.post('/analyze/pdf', response_model=ResumeMatchReport)
async def analyze_pdf(resume_file: UploadFile = File(...), job_description: str = Form(...)):
    return analyzer.evaluate(extract_pdf_text(await resume_file.read()), job_description)
