# Router for analyze function
from fastapi import APIRouter, UploadFile, Form
from services.pdf_processor import pdf_processor
from services.ai_analyzer import ai_analyzer

router = APIRouter()

@router.post("/match_resume")
async def analyze_resume(resume: UploadFile, jd: str = Form(...)):
    pdf_text = await pdf_processor.text_extraction(resume)
    # print(pdf_text[:500])
    ai_results = await ai_analyzer.analyze_resume_with_ai(pdf_text, jd)
    # print(type(ai_results))
    return {"analysis": ai_results}
