import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = (
        "Привет! Я бот для конвертации валют.\n"
        "Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты> <в какую валюту перевести> <количество>\n"
        "Доступные команды:\n"
        "/values — список доступных валют"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = CurrencyConverter.get_available_currencies()
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_currency(message: telebot.types.Message):
    try:
        values = message.text.split()
        
        if len(values) != 3:
            raise APIException("Неверный формат. Должно быть 3 параметра.")
        
        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
        
        text = f"Цена {amount} {base} в {quote} — {total}"
        bot.send_message(message.chat.id, text)
    
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Неожиданная ошибка: {e}")

bot.polling()
