from fastapi import FastAPI, Request, Form
import difflib
import re

app = FastAPI()

# Sample mock data
mafhungo = {
    "love": "U funa",
    "run": "U gidima",
    "play": "U tamba"
}

def vho_ndaa():
    from datetime import datetime
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "Ndi matsheloni 😊 Ndi nga ni thusa hani?"
    elif 11 <= hour < 15:
        return "Ndi masiari 😊 Ndi nga ni thusa hani?"
    elif 15 <= hour < 18:
        return "Ndi mathabama 😊 Ndi nga ni thusa hani?"
    else:
        return "Ndi madekwana 😊 Ndi nga ni thusa hani?"

def ngoma_rich(msg: str) -> str:
    msg = msg.lower().strip()
    ndaa = vho_ndaa()

    # If message says: bvumele <word> tshivenda
    zwikumedzo = re.search(r"bvumele (.+?) tshivenda", msg)
    if zwikumedzo:
        ipfi = zwikumedzo.group(1).strip().lower()
        nga_tsini_na = difflib.get_close_matches(ipfi, mafungo.keys(), n=1)
        hu_shumiswe = mafungo.get(nga_tsini_na[0], "Ndi kha ḓi guda zwenezwo!") if nga_tsini_na else "Ndi kha ḓi guda zwenezwo!"
        return f"{ndaa}\n🟢 \"{ipfi}\" kha Tshivenda = {hu_shumiswe}"

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
        print("🔥 FORM RECEIVED:", dict(form))
        response = ngoma_rich(msg)
        print(f"📤 Responding to {sender} with: {response}")
        return {"response": response}
    except Exception as e:
        print("❌ ERROR:", e)
        return {"error": str(e)}
