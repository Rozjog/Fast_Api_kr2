from fastapi import FastAPI, HTTPException, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import time
from typing import Optional
from itsdangerous import URLSafeSerializer
import json  

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

    current_timestamp = int(time.time()) 
    
    session_data = {
        "user_id": user_id,
        "last_activity": current_timestamp
    }
    
    session_token = serializer.dumps(json.dumps(session_data))

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,   
        max_age=3600,   
        secure=False,     
        samesite="lax"    
    )
    
    return {"message": "Login successful"}

@app.get("/user")
async def get_user(response: Response, session_token: Optional[str] = Cookie(None)):
    if not session_token:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized - No session token"}
        )

    try:
        signed_data = serializer.loads(session_token)
        session_data = json.loads(signed_data)
        
        user_id = session_data.get("user_id")
        last_activity = session_data.get("last_activity")

        if not user_id or not last_activity:
            return JSONResponse(
                status_code=401,
                content={"message": "Unauthorized - Invalid session data"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized - Invalid signature"}
        )
    
    if user_id not in users_db:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized - User not found"}
        )
    
    current_time = int(time.time())

    time_since_last_activity = current_time - last_activity

    THREE_MINUTES = 180
    FIVE_MINUTES = 300

    if time_since_last_activity >= FIVE_MINUTES:
        return JSONResponse(
            status_code=401,
            content={"message": "Session expired"}
        )
    
    if time_since_last_activity >= THREE_MINUTES:
        new_session_data = {
            "user_id": user_id,
            "last_activity": current_time
        }

        new_session_token = serializer.dumps(json.dumps(new_session_data))

        response.set_cookie(
            key="session_token",
            value=new_session_token,
            httponly=True,
            max_age=3600
        )
        
        print(f"Сессия продлена: прошло {time_since_last_activity} сек")
    
    username = users_db[user_id]["username"]

    return {
        "username": username,
        "profile": {
            "username": username,
            "email": f"{username}@example.com"
        }
    }