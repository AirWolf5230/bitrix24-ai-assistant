async def start(update, context):
    user = update.effective_user

    text = (
        f"Привет, {user.first_name}.\n\n"
        "Я бот-ассистент по Bitrix24 API.\n"
        "Задавай вопросы по документации — я отвечу."
    )

    print("========================")
    print(f"Пользователь запустил /start: {user.id}")
    print("========================")

    await update.message.reply_text(text)


async def handle_message(update, context):
    try:
        from app.services.message_service import process_user_message

        user_text = update.message.text

        print("========================")
        print(f"Пользователь: {user_text}")
        print("========================")

        # "думаю..." сообщение
        msg = await update.message.reply_text("Думаю...")

        # LLM + RAG
        answer = await process_user_message(user_text)

        if not answer:
            answer = "Пустой ответ от модели"

        answer = str(answer)

        # защита Telegram лимита
        if len(answer) > 3500:
            answer = answer[:3500] + "\n\n(ответ обрезан)"

        print("\n========================")
        print(f"Ответ: {answer}")
        print("========================\n")

        await msg.edit_text(answer)

    except Exception as e:
        print("ОШИБКА HANDLER:", repr(e))

        try:
            await update.message.reply_text("Ошибка обработки запроса")
        except:
            pass