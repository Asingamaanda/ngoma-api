from fastapi import FastAPI, Request
import difflib
import re

app = FastAPI()

# Dictionary of translations
mafhungo = {
    "ndi a livhuwa": "Thank you",
    "ndi khou neta": "I am tired",
    "ndi khou ṱoḓa u guda": "I want to learn",
    "ndi matsheloni": "Good morning",
    "ndi a ni funa": "I love you",
    "dzina ḽanga ndi": "My name is...",
    "a tho ngo ya": "I didn’t go",
    "vhana vha khou tamba": "They are playing"
}

def ngoma_rich(msg: str) -> str:
    msg = msg.lower().strip()
    ndaa = "Ndi madekwana 😊 Ndi nga ni thusa hani?"

    # Keyword translation
    zwikumedzo = re.search(r"bvumele (.+?) tshivenda", msg)
    if zwikumedzo:
        ipfi = zwikumedzo.group(1).strip().lower()
        nga_tsini_na = difflib.get_close_matches(ipfi, mafhungo.keys(), n=1)
        hu_shumiswe = mafhungo.get(nga_tsini_na[0], "Ndi kha ḓi guda zwenezwo!") if nga_tsini_na else "Ndi kha ḓi guda zwenezwo!"
        return f"{ndaa}\n📘 \"{ipfi}\" kha Tshivenda = {hu_shumiswe}"

    return (
        f"{ndaa}\n"
        "🟢 Zwithu zwine nda nga ita:\n"
        "- Bvuma u amba uri: _“bvumele __ipfi__ tshivenda”_ 🗣️\n"
        "- Ṱoḓa khoroni ya vhutshilo 📖\n"
        "- Ndi nga thusa u nwala nga Tshivenda ✍️\n"
        "- U guda ngahelo ya tshivenda 💬"
    )

# ✅ Twilio sends form-data to /ngoma
@app.post("/ngoma")
async def handle_msg(request: Request):
    try:
        form = await request.form()
        msg = form.get("Body", "")
        return {"response": ngoma_rich(msg)}
    except Exception as e:
        print("💥 ERROR in /ngoma:", e)
        return {"error": str(e)}