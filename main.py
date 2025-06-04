from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    message: str

@app.post("/ngoma")
def handle_msg(data: Input):
    msg = data.message.lower().strip()

    if msg in ["aa", "hello", "ndaa"]:
        return {"response": "Ndi madekwana. Ndi nga ni thusa hani?"}

    if "love" in msg:
        return {"response": "Tshivenda ya 'love' ndi 'U funa'."}

    return {"response": "Ndi kha ḓi guda zwanenzwo! Vhuyani hafhu."}
