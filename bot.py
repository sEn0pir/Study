from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler


QUESTION_1, QUESTION_2, QUESTION_3, RESULTS = range(4)


results = {
    "Раннее утро": "Орёл",
    "Позднее утро": "Медведь",
    "Вечер": "Сова",
    "Активный день": "Лев",
    "Спокойный день": "Панда",
    "Общительный день": "Дельфин"
}

async def start(update: Update, context):
    await update.message.reply_text(
        'Привет! Хотите узнать, какое тотемное животное у вас? Пройдите нашу викторину и получите результат! Нажмите "Начать".',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Начать", callback_data='start')
        ]])
    )

async def question_1(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text('Какое утро вам ближе?', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Раннее утро", callback_data='Раннее утро')],
        [InlineKeyboardButton("Позднее утро", callback_data='Позднее утро')],
        [InlineKeyboardButton("Вечер", callback_data='Вечер')]
    ]))
    return QUESTION_2

async def question_2(update: Update, context):
    query = update.callback_query
    context.user_data['answer_1'] = query.data
    await query.answer()
    await query.edit_message_text('Какой день вам нравится больше?', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Активный день", callback_data='Активный день')],
        [InlineKeyboardButton("Спокойный день", callback_data='Спокойный день')],
        [InlineKeyboardButton("Общительный день", callback_data='Общительный день')]
    ]))
    return QUESTION_3

async def question_3(update: Update, context):
    query = update.callback_query
    context.user_data['answer_2'] = query.data
    await query.answer()
    await query.edit_message_text('Вы любите больше природу или город?', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Природа", callback_data='Природа')],
        [InlineKeyboardButton("Город", callback_data='Город')]
    ]))
    return RESULTS

async def results_handler(update: Update, context):
    query = update.callback_query
    context.user_data['answer_3'] = query.data
    await query.answer()

    answer_1 = context.user_data.get('answer_1')
    animal = results.get(answer_1, "Неизвестное животное")
    await query.edit_message_text(f"Ваше тотемное животное — {animal}!")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text('Викторина прервана. Напишите /start, чтобы начать заново.')
    return ConversationHandler.END

def main():
    TOKEN = "8141785519:AAE_8oI9bxOC8tbh8OuMWx-gL5naGuAH2f0"
    application = Application.builder().token(TOKEN).build()


    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(question_1, pattern='^start$')],
        states={
            QUESTION_2: [CallbackQueryHandler(question_2)],
            QUESTION_3: [CallbackQueryHandler(question_3)],
            RESULTS: [CallbackQueryHandler(results_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
