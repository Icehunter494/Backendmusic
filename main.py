from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

from audio import load_wav
from pitch import analyze_audio

# Create app FIRST
app = FastAPI()

# Then add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://project-zruh1.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    samples, sr = load_wav(path)
    result = analyze_audio(samples, sr)

    return {"notes": result}