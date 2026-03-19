# Импортируем необходимые модули
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
