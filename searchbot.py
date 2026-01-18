import os
from telethon import TelegramClient
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.tl.functions.users import GetFullUserRequest
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

client = TelegramClient("session", api_id, api_hash)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب: /search username")
        return

    q = context.args[0].replace("@", "")
    await client.start()

    try:
        user = await client(GetFullUserRequest(q))
        u = user.users[0]
        text = f"👤 {u.first_name} @{u.username}\n🆔 {u.id}\n\n"
    except:
        text = "❌ لم أستطع جلب معلومات الحساب\n\n"

    result = await client(SearchRequest(
        peer='t.me',
        q=q,
        filter=InputMessagesFilterEmpty(),
        limit=20,
        offset_id=0,
        add_offset=0,
        max_id=0,
        min_id=0,
        hash=0
    ))

    for msg in result.messages:
        try:
            chat = await msg.get_chat()
            if chat.username:
                text += f"📌 {chat.title}\nhttps://t.me/{chat.username}\n\n"
        except:
            pass

    await update.message.reply_text(text)

app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("search", search))
app.run_polling()