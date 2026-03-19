# Импортируем необходимые модули
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime 

app = FastAPI()

class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str


@app.get("/headers")
async def get_headers(
    user_agent: str = Header(..., description="User-Agent header"),
    accept_language: str = Header(..., description="Accept-Language header")
):
    try:
        headers = CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language
        )

        return {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info")
async def get_info(
    response: Response,
    user_agent: str = Header(..., description="User-Agent header"),
    accept_language: str = Header(..., description="Accept-Language header")
):
    try:
        headers = CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language
        )
        response.headers["X-Server-Time"] = datetime.now().isoformat()

        return {
            "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
            "headers": {
                "User-Agent": headers.user_agent,
                "Accept-Language": headers.accept_language
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def root():
    return {
        "example_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
        }
    }