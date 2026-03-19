from fastapi import FastAPI, HTTPException, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from typing import Optional

app = FastAPI()

users_db = {
    "user123": "password123"
}
sessions_db = {}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(response: Response, login_data: LoginData):
    if login_data.username in users_db and users_db[login_data.username] == login_data.password:
        session_token = str(uuid.uuid4())
        sessions_db[session_token] = login_data.username
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600
        )
        
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/user")
async def get_user(session_token: Optional[str] = Cookie(None)):
    if not session_token or session_token not in sessions_db:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized"}
        )
    
    username = sessions_db[session_token]
    return {
        "username": username,
        "profile": {
            "username": username,
            "email": f"{username}@example.ru"
        }
    }