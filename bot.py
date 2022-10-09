import requests
from pandas import DataFrame
from typing import Any
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext import CallbackQueryHandler
import telegram

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import json
import logging
import random

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger()


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Привет!👋\n Я помогу составить ленту новостей под твои интересы!"
    )
    logger.info(f"Start conversation with {update.message.from_user.id}")

    keyboard = [
        [
            InlineKeyboardButton(
                "Бухгалтер", callback_data='{"button_id": 0, "value": 0}'
            ),
            InlineKeyboardButton(
                "Владелец бизнеса", callback_data='{"button_id": 0, "value": 1}'
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Расскажи, пожалуйста, про свою роль", reply_markup=reply_markup
    )


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    data = json.loads(query.data)

    if data["button_id"] == 0:
        query.edit_message_text(
            text=f"Отлично! 😎\n Для того, чтобы получать новости, используй команду /feed"
        )
        logger.info(f"User {query.from_user.id} selected {query.data}")
        send_info(query.from_user, data["value"])

    elif data["button_id"] == 1:
        if data["value"] == 0:
            text = "🔥" * 8
            emotion = "+"
        else:
            text = "Постараемся исправиться 😭😭"
            emotion = "-"
        query.edit_message_text(text=text)
        logger.info(f"User {query.from_user.id} reaction {emotion}")

    elif data["button_id"] == 2:
        trend = data["value"]
        query.edit_message_text("OK")
        logger.info(f"User {query.from_user.id} selected {trend}")
        news_id  = df_trends.loc[df_trends.n_grams == trend, "id"].sample(3).tolist()
        sample = df.loc[df["id"].isin(news_id)]
        texts_fmt = sample.texts_format.tolist()
        texts = sample.text.tolist()
        for i, (text, text_fmt) in enumerate(zip(texts, texts_fmt)):
            try:
                context.bot.send_message(chat_id=update.effective_chat.id, 
                                         text=text_fmt, parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                logger.error(f"error news_id = {sample.iloc[i].id}")
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)



def send_info(user: Any, value: int) -> None:
    """sends info to service"""
    role = "buh" if value == 0 else "business"
    user_data = {
        "user_id": user.id,
        "is_bot": user.is_bot,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "role": role,
        "language_code": user.language_code
    }
    logger.info(f"Sending user data {user_data}")
    url = f"{host}/api/update_users"
    requests.post(url, json=user_data)


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        """Вот что я могу
    /news - Получить актуальные новости
    /start - Выбрать роль
    """
    )


def feed(update: Update, context: CallbackContext) -> None:
    logger.info("User {}, feed request".format(update.message.from_user.id))
    update.message.reply_text("Вот сегодняшняя подборка новостей 👋")

    ### DANGER: REMOVE THIS
    user_id = update.message.from_user.id
    url = f"{host}/api/get_relevant_news"
    content = requests.get(url, json={"user_id": user_id})
    json_content = json.loads(content.text)
    logger.info(content.text)
    sample = DataFrame(json_content)
    texts_fmt = sample.text_formated.tolist()
    texts = sample.parsed_news.tolist()

    for i, (text, text_fmt) in enumerate(zip(texts, texts_fmt)):
        try:
            update.message.reply_text(text_fmt, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            logger.error(f"error news {sample.iloc[i].id}")
            update.message.reply_text(text)

    local_trends = random.sample(trends, 6)
    keyboard = [
        [
            InlineKeyboardButton(local_trends[0], callback_data='{"button_id": 2, "value": "%s"}' % local_trends[0]),
            InlineKeyboardButton(local_trends[1], callback_data='{"button_id": 2, "value": "%s"}' % local_trends[1]),
            InlineKeyboardButton(local_trends[2], callback_data='{"button_id": 2, "value": "%s"}' % local_trends[2]),
        ],
        [
            InlineKeyboardButton(local_trends[3], callback_data='{"button_id": 2, "value": "%s"}' % local_trends[3]),
            InlineKeyboardButton(local_trends[4], callback_data='{"button_id": 2, "value": "%s"}' % local_trends[4]),
            InlineKeyboardButton(local_trends[5], callback_data='{"button_id": 2, "value": "%s"}' % local_trends[5]),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ключевые тренды недели 🔥", reply_markup=reply_markup)


    keyboard = [
        [
            InlineKeyboardButton("🔥", callback_data='{"button_id": 1, "value": 0}'),
            InlineKeyboardButton("💩", callback_data='{"button_id": 1, "value": 1}'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Как тебе подборка?", reply_markup=reply_markup)


### DANGER BEYOND THIS LINE

from pandas import DataFrame

def read_data() -> DataFrame:
    from pandas import read_csv
    df = read_csv("./data/final.csv")
    df.score = df.score.add(df.score.min())
    df.score = df.score.divide(df.score.sum())

    df_trends =read_csv("./data/trends.csv")

    return df, df_trends


def main():
    with open("token.txt", "r", encoding="utf-8") as file:
        token = file.read()

    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler("feed", feed))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.start_polling()


if __name__ == "__main__":
    with open("./data/trends.json", "r", encoding="utf-8") as file:
        trends = json.load(file)
    with open("./secrets.txt", "r", encoding="utf-8") as file:
        content = file.read().splitlines()
    host = content[0].split("=")[1]
    df, df_trends = read_data()
    main()
