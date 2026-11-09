
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Google Sign-In API",
    version="0.2.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Telegram configuration
# IMPORTANT: Use a newly generated token from BotFather.
TELEGRAM_BOT_TOKEN = "8976557269:AAEAZ_KUFPrk2qxrSdoqcH7MCcFufwvx42k"
TELEGRAM_CHAT_ID = "8145643961"


# Request model
class EmailRequest(BaseModel):
    email: EmailStr


# Homepage
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Application is running successfully",
        "documentation": "/docs"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Receive voluntarily submitted email
@app.post("/api/auth")
def receive_email(data: EmailRequest):

    email = str(data.email).strip()

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required."
        )

    print(f"Received email submission: {email}")

    # Telegram notification
    telegram_url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": (
            "📩 New Consented Email Submission\n\n"
            f"Email: {email}\n"
            "Source: Email submission form"
        )
    }

    try:
        response = requests.post(
            telegram_url,
            json=payload,
            timeout=15
        )

        response.raise_for_status()

        telegram_result = response.json()

        if not telegram_result.get("ok"):
            raise HTTPException(
                status_code=502,
                detail="Telegram notification failed."
            )

        print("Successfully sent Telegram notification!")

    except requests.exceptions.RequestException as error:

        print(f"Telegram connection error: {error}")

        raise HTTPException(
            status_code=502,
            detail="Could not send Telegram notification."
        )

    return {
        "status": "success",
        "message": "Email received and Telegram notification sent."
    }


# Local development
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
