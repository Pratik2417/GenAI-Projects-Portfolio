from src.schemas import ResumeMatchReport

def test_structured_output_contract():
    report = ResumeMatchReport(overall_match_score=88, estimated_years_experience=2.5, matched_skills=['Python', 'LangChain', 'FastAPI'], missing_skills=['Kubernetes'], candidate_strengths=['Production RAG pipelines'], improvement_suggestions=['Add latency metrics'], hiring_recommendation='Strong Fit')
    assert report.overall_match_score == 88 and report.estimated_years_experience == 2.5
