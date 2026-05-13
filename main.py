from fastapi import FastAPI, UploadFile, File
import shutil
from audio import load_wav
from pitch import analyze_audio

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    samples, sr = load_wav(path)
    result = analyze_audio(samples, sr)

    return {"notes": result}