from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze
from PyPDF2 import PdfReader

app = FastAPI(title="Resume Consultant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "root"}
