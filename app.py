import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS so your frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your valid token from BotFather and your chat ID
TELEGRAM_BOT_TOKEN = "8976557269:AAEAZ_KUFPrk2qxrSdoqcH7MCcFufwvx42k"
TELEGRAM_CHAT_ID = "8145643961"

class EmailRequest(BaseModel):
    email: str

@app.post("/api/auth")
def receive_email(data: EmailRequest):
    if not data.email:
        raise HTTPException(status_code=400, detail="Email is required.")
        
    print(f"Received Email: {data.email}")
    
    # Construct the Telegram API URL
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Message payload
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"📩 New Submission:\nEmail: {data.email}"
    }
    
    try:
        # Send notification to Telegram
        response = requests.post(telegram_url, json=payload)
        
        if response.status_code != 200:
            print(f"Telegram API Error: {response.text}")
        else:
            print("Successfully sent to Telegram!")
            
    except Exception as error:
        print(f"Failed to connect to Telegram: {error}")
    
    return {
        "status": "success",
        "message": f"Successfully received email: {data.email}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)