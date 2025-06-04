from fastapi import FastAPI, Request
import difflib
import re

app = FastAPI()

def ngoma_rich(msg: str) -> str:
    msg = msg.lower().strip()
    ndaa = "Ndi madekwana 😊 Ndi nga ni thusa hani?"

    # Responses
    if "netisa" in msg or "neta" in msg:
        return f"{ndaa}\nAwu! Zwavhuḓi. Ri pfe khoroni kana ri ite mutambo?"

    if "takala" in msg or "ḓiphina" in msg:
        return f"{ndaa}\nNdi a takala! Nga ri nwaleni thothokiso ya tshivenda."

    if "mbudze khoroni" in msg:
        return (
            f"{ndaa}\n🦁 _Ṋdou o vha e khosi ya zwifuwo. Ṱharu ya vhunga ya mu zwala a tevhela mivhili yayo._\n"
            "Ṱharu a ri: 'Mmbwa ine ya ṱoḓa u vhulaha muthu, i thoma ya kuvhangana na muya wayo.'\n"
            "Ṋdou ya ela mbilu. U ṱoḓa uri ndi bvele phanḓa?"
        )

    if "nthuse u nwala" in msg:
        return f"{ndaa}\nNdi ṱoḓa:\n1️⃣ Muthu (mutukana, musidzana, mukalaha)\n2️⃣ Nḓila (thavha, tsini, muḓi)\n3️⃣ Khombo (o lahlela tshithu, u ṱoḓa ngoho, u pfa ndala)"

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

    zwikumedzo = re.search(r"bvumele (.+?) tshivenda", msg)
    if zwikumedzo:
        ipfi = zwikumedzo.group(1).strip().lower()
        nga_tsini_na = difflib.get_close_matches(ipfi, mafhungo.keys(), n=1)
        hu_shumiswe = mafhungo.get(nga_tsini_na[0], "Ndi kha ḓi guda zwenezwo!") if nga_tsini_na else "Ndi kha ḓi guda zwenezwo!"
        return f"{ndaa}\n📗 \"{ipfi}\" kha Tshivenda = {hu_shumiswe}"

    return (
        f"{ndaa}\n"
        "🟢 Zwithu zwine nda nga ita:\n"
        "- Bvuma u amba uri: _“bvumele __ipfi__ tshivenda”_ 🗣️\n"
        "- Ṱoḓa khoroni ya vhutshilo 📖\n"
        "- Ndi nga thusa u nwala nga Tshivenda ✍️\n"
        "- U guda nga ngahelo ya tshivenda 💬"
    )

# ✅ Twilio sends form-data
@app.post("/ngoma")
async def handle_msg(request: Request):
    form = await request.form()
    msg = form.get("Body", "")
    return {"response": ngoma_rich(msg)}

   
