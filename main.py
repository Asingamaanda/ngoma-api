from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import difflib
import re

app = FastAPI()

# Sample dictionary for demonstration (replace with your own logic)
mafungo = {
    "love": "U funa",
    "thank you": "Ro livhuwa",
    "help": "Ndi nga ni thusa hani?",
}

def ngoma_rich(msg: str) -> str:
    msg = msg.strip().lower()
    ndaa = "Ndi madekwana 😊 Ndi nga ni thusa hani?"

    # Detect Tshivenda trigger
    zwikumedzo = re.search(r"bvumele (.+?) tshivenda", msg)
    if zwikumedzo:
        ipfi = zwikumedzo.group(1).strip().lower()
        nga_tsini_na = difflib.get_close_matches(ipfi, mafungo.keys(), n=1)
        hu_shumiswe = mafungo.get(nga_tsini_na[0], "Ndi kha ḓi guda zwenezwo!") if nga_tsini_na else "Ndi kha ḓi guda zwenezwo!"
        return f"{ndaa}\n🟩 \"{ipfi}\" kha Tshivenda = {hu_shumiswe}"

    # Default options
    return (
        f"{ndaa}\n"
        "🟢 Zwithu zwine nda nga ita:\n"
        "- Bvuma u amba uri: _“bvumele __ipfi__ tshivenda”_ 🗣️\n"
        "- Ṱoḓa khoroni ya vhutshilo 📖\n"
        "- Ndi nga thusa u nwala nga Tshivenda ✍️\n"
        "- U guda nga ngahelo ya tshivenda 💬"
    )

@app.post("/ngoma")
async def handle_msg(request: Request):
    try:
        form = await request.form()
        msg = form.get("Body", "")
        sender = form.get("From", "")
        print(f"🔥 FORM RECEIVED from {sender} with message: {msg}")
        reply = ngoma_rich(msg)
        print(f"📤 Responding to {sender} with:\n{reply}")
        return PlainTextResponse(reply)
    except Exception as e:
        print("❌ ERROR:", e)
        return PlainTextResponse("Internal Server Error", status_code=500)
