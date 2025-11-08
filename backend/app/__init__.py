from fastapi import FastAPI, UploadFile, File
from .ade_client import parse_document

app = FastAPI()

@app.post("/api/parse")
async def parse_file(file: UploadFile = File(...)):
    content = await file.read()
    result = parse_document(content, file.filename)
    return result
