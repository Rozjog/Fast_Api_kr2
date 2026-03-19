from fastapi import FastAPI, HTTPException, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from typing import Optional
from itsdangerous import URLSafeSerializer

app = FastAPI()

users_db = {
    "123e4567-e89b-12d3-a456-426614174000": {
        "username": "user123",
        "password": "password123"
    }
}

username_to_uuid = {
    "user123": "123e4567-e89b-12d3-a456-426614174000"
}

SECRET_KEY = "my-super-secret-key-12345"
serializer = URLSafeSerializer(SECRET_KEY)

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(response: Response, login_data: LoginData):
    if login_data.username not in username_to_uuid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = username_to_uuid[login_data.username]

    if users_db[user_id]["password"] != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_token = serializer.dumps(user_id)
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=3600
    )
    
    return {"message": "Login successful"}

@app.get("/user")
async def get_user(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    
    try:
        user_id = serializer.loads(session_token)
    except Exception:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    if user_id not in users_db:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    username = users_db[user_id]["username"]
    
    return {
        "username": username,
        "profile": {
            "username": username,
            "email": f"{username}@example.com"
        }
    }