import json, asyncio
from random import choice
from datetime import datetime
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import dp, bot
from config import ADMIN_IDS

def load_db():
    try:
        return json.load(open("db.json", encoding="utf-8"))
    except:
        return {"participants": []}
def save_db(data):
    json.dump(data, open("db.json", "w", encoding="utf-8"), indent=2)
def load_winners():
    try:
        return json.load(open("winners.json", encoding="utf-8"))
    except:
        return []
def save_winners(data):
    json.dump(data, open("winners.json", "w", encoding="utf-8"), indent=2)

@dp.message_handler(commands=["start"])
async def cmd_start(msg: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🎁 Участвовать", callback_data="join"))
    await msg.answer("Нажми кнопку, чтобы участвовать!", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data=="join")
async def cb_join(c: types.CallbackQuery):
    db = load_db()
    uid = c.from_user.id
    if uid not in db["participants"]:
        db["participants"].append(uid)
        save_db(db)
        await c.message.answer("✅ Ты в игре!")
    else:
        await c.message.answer("❗ Ты уже учаешься.")

@dp.message_handler(commands=["set_timer"])
async def cmd_set_timer(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        await msg.reply("⛔ Ты не админ.")
        return
    try:
        mins = int(msg.get_args())
        await msg.reply(f"⏳ Старт через {mins} минут.")
        await asyncio.sleep(mins*60)
        await run_giveaway(msg)
    except:
        await msg.reply("❗ /set_timer <минуты>")

@dp.message_handler(commands=["winners"])
async def cmd_winners(msg: types.Message):
    history = load_winners()
    if not history:
        await msg.answer("🏅 Побед не было.")
        return
    txt = "🏅 Победители:
" + "\n".join(
        f"[{w['winner_id']}](tg://user?id={w['winner_id']}) — {w['date']}" 
        for w in history[-5:]
    )
    await msg.answer(txt, parse_mode="Markdown")

async def run_giveaway(msg: types.Message):
    db = load_db()["participants"]
    if not db:
        await msg.reply("Нет участников.")
        return
    winner = choice(db)
    await bot.send_message(winner, "🎉 Ты победил!")
    await msg.answer(f"🎉 Победитель — [{winner}](tg://user?id={winner})", parse_mode="Markdown")
    save_db({"participants": []})
    history = load_winners()
    history.append({"winner_id": winner, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
    save_winners(history)