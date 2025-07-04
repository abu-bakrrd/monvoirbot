import os
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
ADMIN_CHAT_ID = 5644397480  # Замени на свой ID

@bot.message_handler(commands=['about'])
def about_handler(message):
    about_text = """
<b>🛍 О магазине MONVOIR</b>

Мы — бренд стильной одежды, созданный для тех, кто ценит качество, моду и комфорт.  
Работаем по всей территории Узбекистана. Новинки добавляются каждый день!

<b>📦 Доставка:</b>  
— По Узбекистану  
— Самовывоз / Курьер / Почта

<b>📲 Связь:</b>  
Для связи с нами — используйте команду /support

<i>Будь в стиле. Будь с MONVOIR.</i>
"""
    bot.send_message(message.chat.id, about_text, parse_mode='HTML')

@bot.message_handler(commands=['support'])
def support_command(message):
    bot.send_message(
        message.chat.id,
        "✉️ Напиши свой вопрос или сообщение, и я передам его в службу поддержки."
    )
    bot.register_next_step_handler(message, forward_to_admin)

def forward_to_admin(message):
    user = message.from_user
    text = f"📩 Новое сообщение от @{user.username or 'без username'} (ID: {user.id}):\n\n{message.text}"
    bot.send_message(ADMIN_CHAT_ID, text)
    bot.send_message(message.chat.id, "✅ Спасибо! Ваше сообщение отправлено в поддержку.")

@bot.message_handler(commands=['start'])
def handle_start(message):
    args = message.text.split()
    if len(args) != 2:
        WELCOME_TEXT = """
👋 <b>Добро пожаловать в MONVOIR!</b>

🖤 Здесь ты найдёшь стильную одежду и актуальные новинки.

<b>📌 Команды:</b>
/support – написать в поддержку  
/about – информация о магазине

📦 Мы доставляем по всему Узбекистану!

<b>🛒 Готов заказать?</b>  
Нажимай <b>Open Store</b> снизу и оформляй заказ прямо в Telegram!

<i>Будь в стиле, будь с MONVOIR.</i>    
"""
        bot.send_message(message.chat.id, WELCOME_TEXT, parse_mode="HTML")
        return

    msg = bot.send_message(message.chat.id, '<i>Проверяем подлинность...</i>', parse_mode="HTML")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('monvoir-8bb20faac9b5.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("Monvoir orders")
    sheet = spreadsheet.get_worksheet(2)

    param = args[1]
    if not param.startswith("order_"):
        bot.send_message(message.chat.id, "⚠ Неверный формат кода.")
        return

    unique_code = param.replace("order_", "").strip()

    try:
        records = sheet.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row['uniquie_code']).strip() == unique_code:
                if str(row['yes/no']).strip().lower() == "yes":
                    bot.send_message(message.chat.id, "⚠ Этот код уже был использован.")
                else:
                    sheet.update_cell(i, 3, str(message.from_user.id))
                    sheet.update_cell(i, 4, "yes")
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text="✅ Код подтверждён. Спасибо за покупку!")
                return
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text="❌Такой код не найден.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

# 🔁 Включаем polling
if __name__ == '__main__':
    print("🤖 Бот запущен (polling)...")
    bot.infinity_polling()
