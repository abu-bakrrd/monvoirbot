import telebot

# Инициализация
TOKEN = '7751530491:AAGmzfztRlNOUJ5CPMvkDMSmBSj6a3Xph_U'
bot = telebot.TeleBot(TOKEN)
ADMIN_CHAT_ID = 5644397480  # Замени на свой ID
# Команды
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

def run_bot():
    while True:
        try:
            print("Запускаю бота...")
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Перезапуск через 5 секунд...")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()


