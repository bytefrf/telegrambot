import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# Список записок

# Список записок
easy_notes = [
    "Архивный документ A1: Примечания к жалобе 1\n"
    '"Жалоба направлена в комитет по этике, но не получила ответа.\n'
    'Копии расчётных листов подтверждают снижение зарплаты."',

    "Архивный документ A2: Примечания к отчёту 2\n"
    '"Инициатор — комитет, но решение о сокращениях принимал ФД."',
]
hard_notes = [
    "Архивный документ A1: Примечания к жалобе 1\n"
    '"Жалоба направлена в комитет по этике, но не получила ответа.\n'
    'Копии расчётных листов подтверждают снижение зарплаты."',

    "Архивный документ A2: Примечания к отчёту 2\n"
    '"Инициатор — комитет, но решение о сокращениях принимал ФД."',

    "Архивный документ A3: Примечания к IT-журналу 3\n"
    '"Сбои были ложными: серверы работали стабильно. Жалоба — отвлекающий манёвр."',

    "Архивный документ A4: Ключ к шифру 4\n"
    '"Сообщение зашифровано методом Цезаря (сдвиг на 3 буквы).\n'
    'Расшифровка:\n'
    'Начните сокращения в отделе разработки. Говорите, что позиции упразнены, но не оформляйте это в документах. Срочно. — ИВ"',

    "Архивный документ A5: Примечания к жалобе 5\n"
    '"Жалобы на CEO — не основная причина ухода сотрудников.\n'
    'Смирнов не участвовал в сокращениях."',

    "Архивный документ A6: Протокол комитета 13\n"
    '"На заседании 01.01.2023:\n'
    '- Иван Сидоров предложил сократить зарплаты.\n'
    '- Олег Фёдоров выступил против, но согласился при угрозе увольнения."',

    "Архивный документ A7: Примечания к финансам 7\n"
    '"ИИ-проект был отменён в феврале 2023, но средства не были возвращены в бюджет."',

    "Архивный документ A8: Код к переписке 18\n"
    '"Сообщение Фёдорова зашифровано. Ключ: \'ФД\' (расшифровка:\n'
    'Проект "Феникс" — фикция. Средства на мой счёт. Уничтожьте следы. — ОФ)"',

    "Архивный документ A9: Примечания к кибератаке 14\n"
    '"Хакерская атака — выдумка. Жалоба направлена для отвлечения внимания."',

    "Архивный документ A10: Протокол серверов 17\n"
    '"Попытки доступа — фальшивые. Их добавил кто-то из высшего руководства."',

    "Архивный документ A11: Примечания к резюме 11\n"
    '"20 сотрудников написали аналогичные резюме.\n'
    'Это шаблонная форма, но причины повторяются."',

    "Архивный документ A12: Примечания к финансам 20\n"
    '"Проект \'Феникс\' не существует. Средства были выведены через подставную фирму."',

    "Архивный документ A13: Переписка между ФД и ТД\n"
    '"Кому: Олег Фёдоров\n'
    'От: Иван Сидоров\n'
    'Тема: Срочно!\n'
    'Если не поддержите проект "Феникс", я обвиню вас в хищении. — ИС"',

    "Архивный документ A14: Дополнение к жалобе 5\n"
    '"Ольга Ковалева уволена в марте 2023. Её отдел не связан с массовыми увольнениями."',

    "Архивный документ A15: Протокол увольнений 6\n"
    '"Увольнения в отделе разработки связаны с давлением ФД, а не реорганизацией."',
]
# Словарь для хранения состояния игры каждого пользователя
user_states = {}
# Словарь для хранения собранных записок
user_notes = {}

# Функция для старта бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот-игра. Твоя цель — собрать все записки, играя в игру 'Угадай число'.\n"
        "Выбери уровень сложности:\n"
        "/easy — Лёгкий (число от 1 до 10, 7 попыток, доступны только 2 записки)\n"
        "/medium — Средний (число от 1 до 20, 5 попыток, доступны все записки)\n"
        "/hard — Сложный (число от 1 до 50, 3 попытки, доступны все записки)"
    )

# Функция для начала игры (лёгкий уровень)
async def easy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id in user_notes and len(user_notes[user_id]) >= len(easy_notes):
        await update.message.reply_text("Ты уже собрал все лёгкие записки!")
        return
    await start_game(update, 1, 10, 7, is_easy=True)

# Функция для начала игры (средний уровень)
async def medium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_game(update, 1, 20, 5, is_easy=False)

# Функция для начала игры (сложный уровень)
async def hard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_game(update, 1, 50, 3, is_easy=False)

# Вспомогательная функция для старта игры
async def start_game(update: Update, min_num: int, max_num: int, attempts: int, is_easy: bool) -> None:
    user_id = update.message.from_user.id
    target_number = random.randint(min_num, max_num)
    user_states[user_id] = {"target_number": target_number, "attempts_left": attempts, "is_easy": is_easy}
    await update.message.reply_text(
        f"Я загадал число от {min_num} до {max_num}. У тебя {attempts} попыток. Попробуй угадать!"
    )
# Функция для обработки сообщений от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text.strip()

    # Проверяем, начал ли пользователь игру
    if user_id not in user_states:
        await update.message.reply_text("Сначала начни игру командой /easy, /medium или /hard.")
        return

    # Проверяем, является ли сообщение числом
    if not user_message.isdigit():
        await update.message.reply_text("Пожалуйста, введи число.")
        return

    guess = int(user_message)
    state = user_states[user_id]
    state["attempts_left"] -= 1

    # Проверяем, угадал ли пользователь число
    if guess == state["target_number"]:
        # Определяем доступные записки
        if state["is_easy"]:
            available_notes = [n for n in easy_notes if n not in user_notes.get(user_id, set())]
        else:
            available_notes = [n for n in hard_notes if n not in user_notes.get(user_id, set())]

        # Проверяем, есть ли доступные записки
        if not available_notes:
            await update.message.reply_text("Ты уже собрал все доступные записки на этом уровне!")
            del user_states[user_id]
            return

        # Выбираем случайную записку
        note = random.choice(available_notes)

        # Добавляем записку в список собранных
        if user_id not in user_notes:
            user_notes[user_id] = set()
        user_notes[user_id].add(note)

        # Отправляем записку пользователю
        await update.message.reply_text(f"Поздравляю! Ты угадал!\nТвоя записка: {note}")
        del user_states[user_id]  # Удаляем состояние игры

    elif state["attempts_left"] <= 0:
        await update.message.reply_text(f"К сожалению, ты проиграл. Загаданное число было {state['target_number']}.")
        del user_states[user_id]
    else:
        # Подсказки
        if abs(guess - state["target_number"]) > 5:
            hint = "Очень далеко!"
        elif abs(guess - state["target_number"]) <= 2:
            hint = "Ты почти у цели!"
        else:
            hint = "Близко, но не совсем."

        await update.message.reply_text(
            f"{hint}\n"
            f"Моё число {'больше' if guess < state['target_number'] else 'меньше'}. "
            f"Осталось попыток: {state['attempts_left']}. Попробуй ещё раз!"
        )
        
  #Функция для просмотра собранных записок
async def collected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_notes or not user_notes[user_id]:
        await update.message.reply_text("У тебя пока нет собранных записок. Начни игру командой /easy, /medium или /hard.")
        return

    collected_notes = "\n\n".join(user_notes[user_id])
    await update.message.reply_text(f"Твои собранные записки:\n\n{collected_notes}")

# Основная функция для запуска бота
def main() -> None:
    token = "7763883072:AAFIEhyClrIDLWmfHVNIymVtHvGz0db1Arc"

    # Создание приложения
    application = Application.builder().token(token).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("easy", easy))
    application.add_handler(CommandHandler("medium", medium))
    application.add_handler(CommandHandler("hard", hard))
    application.add_handler(CommandHandler("collected", collected))

    # Регистрация обработчика текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()