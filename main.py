import asyncio
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from os import environ as env
markdown = enums.ParseMode.MARKDOWN
html = enums.ParseMode.HTML

api_id = int(env.get('API_ID'))
api_hash = env.get('API_HASH')
bot_token = env.get('BOT_TOKEN')
chatID = int(env.get('CHAT_ID'))

app = Client('AIExplorer', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command('start'))
async def start(client, message):
    try:
        while True:
            url = "https://theresanaiforthat.com/"
            req = requests.get(url)
            soup = BeautifulSoup(req.content, "html.parser")

            new_ones = soup.find("div", {"class": "tasks"})
            products = new_ones.find_all("li")
            for product in products:
                name = product.find("div", {"class": "ai_link_wrap"}).find("a").text.strip()
                link = product.get("data-url")
                category = product.find("div", {"class": "task_label_wrap"}).text.strip()
                published = product.find("div", {"class": "available_starting"}).text.replace("Share","").strip()
                published_date = datetime.strptime(published, "%d %b %Y").strftime('%d %m %Y')
                today = datetime.today().strftime('%d %m %Y')
                button = [[InlineKeyboardButton(name, url=link)]]
                if today in published_date:
                    await app.send_message(
                        chatID,
                        f"<b>YENİ!</b>\n\n<b>Adı:</b> <a href={link}>{name}</a>\n<b>Kategori:</b> #{category.replace(' ', '')}\n<b>Yayınlanma Tarihi:</b> {published}",
                        disable_web_page_preview=False,
                        parse_mode=html,
                        reply_markup=InlineKeyboardMarkup(button))
                    await asyncio.sleep(3)
            time.sleep(10800)
            
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {e}")
    
app.run()
