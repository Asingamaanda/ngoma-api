
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    message: str

@app.post("/test-ngoma")
def handle_msg(data: Input):
    msg = data.message.lower().strip()
    if msg in ["aa", "ndaa", "avuxeni", "hello"]:
        return {"response": "Ndi madekwana 😊 Ndi nga ni thusa nga mini?"}
    if "nga ni thusa nga mini" in msg or msg.startswith("ndi nga ni thusa"):
        return {"response": (
            "🟢 Khezwi zwine nda nga ni thusa ngazwo:
"
            "- Bvumele ipfi tshivenda 🗣️ (e.g. bvumele 'i love you' tshivenda)
"
            "- Ṱoḓa khoroni ya vhutshilo 📖 (e.g. mbudze khoroni)
"
            "- U guda ngahelo: muṱa, tshifhinganyana, u landula 💬
"
            "- Ndi nga thusa u nwala nga Tshivenda ✍️"
        )}
    return {"response": "Ndi kha ḓi guda. Kha ni tonde u vhudzisa futu!"}
