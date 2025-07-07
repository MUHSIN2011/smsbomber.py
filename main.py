# To run this code, make sure you have installed pyrogram and tgcrypto:
# pip install pyrogram tgcrypto

from pyrogram import Client, filters
import asyncio
import time



api_id = 22884594  # API_ID-и худро ин ҷо гузор
api_hash = "029a226c0c430b9f095f57303e52cab6"  # API_HASH-и худро ин ҷо гузор
last_active = {}  # chat_id -> last active timestamp
bot_token = "7741095182:AAFHmPfDrRjypuVqjLOOFKihzO6V5vSh5JM"  # 🔁 токени боти Telegram-и худ

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# Шрифтҳо
user_fonts = {}  # chat_id -> selected_font

def to_fancy(text):
    fancy_map = {
        'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': '𝑒', 'f': '𝒻', 'g': '𝑔', 'h': '𝒽',
        'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃', 'o': '𝑜', 'p': '𝓅',
        'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊', 'v': '𝓋', 'w': '𝓌', 'x': '𝓍',
        'y': '𝓎', 'z': '𝓏', ' ': ' '
    }
    return ''.join(fancy_map.get(c, c) for c in text.lower())

def to_bold(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘶𝘷𝘄𝘅𝘺𝘇"))

def to_italic(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"))

def to_bold_italic(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯"))

def to_monospace(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"))

def to_script(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"))

# 🔤 Шрифтҳои нав
def to_vaporwave(text):
    return ''.join(chr(ord(c) + 0xFEE0) if '!' <= c <= '~' else c for c in text)

def to_glitch(text):
    return ''.join(f"{c}\u0336" for c in text)

def to_mirrored(text):
    mirror_map = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ɐqɔpǝɟƃɥᴉɾʞʃɯuodbɹsʇnʌʍxʎz")
    return text.translate(mirror_map)

def to_outline(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"))

def to_circled(text):
    circle_map = dict(zip("abcdefghijklmnopqrstuvwxyz", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"))
    return ''.join(circle_map.get(c, c) for c in text.lower())

def to_smallcaps(text):
    return ''.join({'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
                    'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
                    'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
                    'y': 'ʏ', 'z': 'ᴢ'}.get(c, c) for c in text.lower())

def to_gothic(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"))

def to_double(text):
    return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"))

def to_tiny(text):
    return ''.join({'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ', 'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ',
                    'i': 'ᶦ', 'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ', 'p': 'ᵖ',
                    'q': 'ᑫ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ', 'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ',
                    'y': 'ʸ', 'z': 'ᶻ'}.get(c, c) for c in text.lower())

# Фармони /font
@app.on_message(filters.command("font"))
async def font_command(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply(
            "📚 Шрифтҳоро санҷ:\n\n"
            f"{to_fancy('шрифт')}  →  /font fancy\n"
            f"{to_bold('bold')}  →  /font bold\n"
            f"{to_italic('italic')}  →  /font italic\n"
            f"{to_bold_italic('bolditalic')}  →  /font bold_italic\n"
            f"{to_monospace('monospace')}  →  /font monospace\n"
            f"{to_script('script')}  →  /font script\n"
            f"{to_vaporwave('vaporwave')}  →  /font vaporwave\n"
            f"{to_glitch('glitch')}  →  /font glitch\n"
            f"{'m̲i̲r̲r̲o̲r̲e̲d̲'}  →  /font mirrored\n"
            f"{to_outline('outline')}  →  /font outline\n"
            f"{to_circled('circled')}  →  /font circled\n"
            f"{to_smallcaps('smallcaps')}  →  /font smallcaps\n"
            f"{to_gothic('gothic')}  →  /font gothic\n"
            f"{to_double('DOUBLE')}  →  /font double\n"
            f"{to_tiny('tiny')}  →  /font tiny\n"
            f"{'⒫⒜⒭⒠⒩⒯⒣⒠⒮⒤⒵⒠⒟'}  →  /font parenthesized\n"
            f"{'ｆｕｌｌｗｉｄｔｈ'}  →  /font fullwidth\n"
            f"{'ˢᵘᵖᵉʳˢᶜʳᶦᵖᵗ'}  →  /font superscript\n"
            f"{'ₛᵤᵦₛᶜᵣᵢₚₜ'}  →  /font subscript"
        )
        return

    font = args[1].lower()
    if font not in available_fonts:
        await message.reply("❌ Шрифт вуҷуд надорад.\nБо /font бидуни параметр шрифтҳоро бубин.")
        return

    user_fonts[message.chat.id] = font
    await message.reply(f"✅ Шрифт ба `{font}` иваз шуд.")


# Ҳамаи шрифтҳо
available_fonts = {
    "fancy": to_fancy,
    "bold": to_bold,
    "italic": to_italic,
    "bold_italic": to_bold_italic,
    "monospace": to_monospace,
    "script": to_script,
    "vaporwave": to_vaporwave,
    "glitch": to_glitch,
    "mirrored": to_mirrored,
    "outline": to_outline,
    "circled": to_circled,
    "smallcaps": to_smallcaps,
    "gothic": to_gothic,
    "double": to_double,
    "tiny": to_tiny
}

# Фармонҳо
hack_texts = [
    "☘️ Мо мехохем акаунти шуморо hack кунем 👨‍💻",
    "🥷 Мо акаунти шуморо hack кардем",
    "☎️ Мо номерхои  акаунти шуморо гирифтем ♾️",
    "🎰 Мо ба акаунти шумо код равон кардем 🤞",
    "⏳ Сабр кунед то мо кодро гирем ",
    "👁 Мо кодро гирифтем •••• 🫧",
    "📲 Мо ба акаунти шумо дохил шудем",
    "🗑 Сабр кунед то мо кодро удалит кунем ки шӯмо кодро дида натавонед",
    "😮‍🔥 Акнун шумо зери назорат ҳаст",
    "🚪@muhsin_nazarov хар лахза ба акаунти шумо даромада метавонад",
    "🥴 ва @muhsin_nazarov метавонад ки",
    "😺 хар лахза шуморо аз акаунтатон уд кунад",
    "🔓 бубахшед шумо аз акаунтатон мондед 😁😁😁",
]

prank_texts = [
    "Мо шуморо фиреб додем...😁😁😁",
    "😁😁 Шумо фиреб хурдед, магар намедонистед? ки ин пранк аст",
    "😅 Тамом! Шумо қурбонии як пранки эпик шудед."
]

help_text = """
📘 Рӯйхати пурраи фармонҳо:
• /start - Оғози кор бо бот
• /font [ном] - Иваз кардани шрифт
• /hack - Аниматсияи взлом (пранк)
• /prank - Пранки хандовар
• /help - Ёрии умумӣ

📊 Танзимоти ҷорӣ:
• Шрифт: bold

"""


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Салом! Ман боти @muhsin_nazarov ҳастам. Барои маълумот: /help")

@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply(help_text)

@app.on_message(filters.command("hack"))
async def hack_command(client, message):
    sent = await message.reply(hack_texts[0])
    for i in range(1, len(hack_texts)):
        await asyncio.sleep(2.5)
        await sent.edit_text(hack_texts[i])

@app.on_message(filters.command("prank"))
async def prank_command(client, message):
    sent = await message.reply(prank_texts[0])
    for i in range(1, len(prank_texts)):
        await asyncio.sleep(2.5)
        await sent.edit_text(prank_texts[i])

@app.on_message(filters.text & filters.private)
async def animated_fancy_typing(client, message):
    if message.text.startswith("/"):
        return

    me = await client.get_me()
    if message.from_user.id != me.id:
        # Агар паём аз шахси дигар бошад:
        last = last_active.get(message.chat.id, 0)
        now = time.time()
        if now - last > 1:  # Агар 60 сония ё бештар гузаштааст
            await message.reply("👋 салом ман боти 🤖 @muhsin_nazarov хастам мухсиддин холо онлайн нест 😟 вахте ки онлайн шуд хатман ба шумо чавоб медихад 😇")
        return

    # ✅ Агар паём аз худат бошад — коркард кун
    last_active[message.chat.id] = time.time()  # Вақти охиринро сабт кун
    await message.delete()

    font_name = user_fonts.get(message.chat.id, "fancy")
    converter = available_fonts.get(font_name, to_fancy)
    styled_text = converter(message.text.lower())

    composed = ""
    for char in styled_text:
        composed += char
        await asyncio.sleep(0.1)

    await client.send_message(chat_id=message.chat.id, text=composed)



app.run()
