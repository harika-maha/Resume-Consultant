# Process the pdf files

from PyPDF2 import PdfReader
from fastapi import UploadFile, HTTPException

class PdfProcessor:
    async def text_extraction(self, file: UploadFile):
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        try:
            pdf_content = PdfReader(file.file)
            text = ""
            for page in pdf_content.pages:
                text += page.extract_text() +"\n"

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error processing PDF file")
        return text
    
pdf_processor = PdfProcessor()