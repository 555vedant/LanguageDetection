from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from coordinator import coordinate_detection
import os
import shutil

app = FastAPI()

# Mount static files (optional for future CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates for HTML
templates = Jinja2Templates(directory="templates")

# Ensure audio_files directory exists
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

class DetectionRequest(BaseModel):
    audio_file_path: str
    ground_truth_language: str  # For context only, not used

# API Endpoint for file upload
@app.post("/detect/language")
async def detect_language(ground_truth_language: str = "", file: UploadFile = File(...)):
    try:
        # Save uploaded file to audio_files/
        file_path = os.path.join(AUDIO_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Pass the saved file path to coordinator
        results = coordinate_detection(file_path)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# UI Landing Page (Default Route)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})