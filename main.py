from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from tshivenda_grammar import autocorrect_sentence
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NGOMA AI is alive 🎶"}

@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_reply(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    msg = Body.strip()
    words = msg.split()

    # Grammar correction using noun-verb logic
    if len(words) >= 2:
        subject, verb = words[0], words[1]
        rest = " ".join(words[2:])
        corrected = autocorrect_sentence(subject, verb, rest)
        response_text = f"📝 Ho lulamiswa: {corrected}"
    else:
        response_text = (
            "Ndaa 😊\n"
            "Welcome to NGOMA — Venda’s First AI Voice!\n"
            "📘 Example: 'Tshikolo vho ita mushumo' → We'll fix it for you.\n"
            "💬 Try a sentence in Tshivenda."
        )

    # Build TwiML response
    response = MessagingResponse()
    response.message(response_text)
    return str(response)
