# app.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from model.model import SentimentModel
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import threading

app = FastAPI()
model = SentimentModel()
templates = Jinja2Templates(directory="templates")

# 최신 결과를 저장할 변수와 스레드 안전을 위한 락
latest_result = {"text": "아직 분석된 텍스트가 없습니다.", "sentiment": "알 수 없음"}
lock = threading.Lock()

class TextInput(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict_sentiment(input: TextInput):
    prediction = model.predict(input.text)
    with lock:
        latest_result["text"] = input.text
        latest_result["sentiment"] = prediction
    return {"text": input.text, "sentiment": prediction}

@app.get("/latest", response_class=JSONResponse)
async def get_latest():
    with lock:
        return latest_result
