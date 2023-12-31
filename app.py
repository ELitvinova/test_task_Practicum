from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from random import randint
from dotenv import load_dotenv
from speechapi import speech_to_text
import os


WELCOME_MESSAGE = """Привет! Этот бот сделан @ltvnva в качестве тестового задания.

Что он умеет:
/photo - прислать селфи или фото из старшей школы
/post - показать пост о моем главном увлечении
/voice - прислать войс на одну из трех тем
/git - дать ссылку на публичный репозиторий с исходным кодом

А еще он может распознавать речь. Правда, он знает только одну голосовую команду: "Пришли ссылку на блог". Какой блог? \
Конечно же, мой :)
"""

HELP_MESSAGE = """
Команды, которые знает бот:
/photo - прислать селфи или фото из старшей школы
/post - показать пост о моем главном увлечении
/voice - прислать войс на одну из трех тем
/git - дать ссылку на публичный репозиторий с исходным кодом

Получить ссылку на мой блог: голосовое сообщение с текстом "Пришли ссылку на блог"
"""

SQL_BUTTON_CALLBACK_DATA = "SQL"
GPT_BUTTON_CALLBACK_DATA = "GPT"
LOVE_BUTTON_CALLBACK_DATA = "LOVE"

SELFIE_BUTTON_CALLBACK_DATA = "SELFIE"
SCHOOL_PHOTO_BUTTON_CALLBACK_DATA = "SCHOOL_PHOTO"


SCHOOL_PHOTO_CNT = 3

REPO_LINK = "https://github.com/ELitvinova/test_task_Practicum"


def start_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, text=WELCOME_MESSAGE)


def help_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, text=HELP_MESSAGE)


def photo_command_handler(update, context):
    chat = update.effective_chat
    button_selfie = InlineKeyboardButton(
        text="Последнее селфи",
        callback_data=SELFIE_BUTTON_CALLBACK_DATA
    )
    button_school_photo = InlineKeyboardButton(
        text="Фото из старшей школы",
        callback_data=SCHOOL_PHOTO_BUTTON_CALLBACK_DATA
    )

    context.bot.send_message(
        chat_id=chat.id,
        text='Прислать последнее селфи или фото из старшей школы?',
        reply_markup=InlineKeyboardMarkup([[button_selfie], [button_school_photo]])
    )


def voice_command_handler(update, context):
    chat = update.effective_chat
    button_sql = InlineKeyboardButton(
        text="SQL vs NoSQL",
        callback_data=SQL_BUTTON_CALLBACK_DATA
    )
    button_gpt = InlineKeyboardButton(
        text="Что такое GPT?",
        callback_data=GPT_BUTTON_CALLBACK_DATA
    )
    button_love = InlineKeyboardButton(
        text="История первой любви",
        callback_data=LOVE_BUTTON_CALLBACK_DATA
    )

    context.bot.send_message(
        chat_id=chat.id,
        text='Выбери тему голосового сообщения',
        reply_markup=InlineKeyboardMarkup([[button_sql], [button_gpt], [button_love]])
    )


def selfie_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_PHOTO)
    with open("./photos/selfie.jpg", "rb") as photo:
        context.bot.send_photo(
            chat.id,
            photo,
            caption="Ем яблоко в перерыве между занятиями кайтсерфингом. На заднем плане пасутся коровы")


def school_photo_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_PHOTO)
    photo_id = randint(1, SCHOOL_PHOTO_CNT)
    with open(f"./photos/school{photo_id}.jpg", "rb") as photo:
        context.bot.send_photo(
            chat.id,
            photo,
            caption="Одна из рандомных фотографий из школы")


def sql_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_VOICE)
    with open("./voices/voice_sql.ogg", "rb") as audio:
        context.bot.send_voice(
            chat.id,
            audio,
            caption="Разница между SQL и NoSQL")


def gpt_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_VOICE)
    with open("./voices/voice_gpt.ogg", "rb") as audio:
        context.bot.send_voice(
            chat.id,
            audio,
            caption="Что такое GPT?")


def love_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_VOICE)
    with open("./voices/voice_love.ogg", "rb") as audio:
        context.bot.send_voice(
            chat.id,
            audio,
            caption="История первой любви")


def git_command_handler(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, text=f"Ссылка на репозиторий с исходным кодом бота: {REPO_LINK}")


def post_command_handler(update, context):
    chat = update.effective_chat
    post_text = ""
    with open("./post.txt", "r") as post_file:
        post_text = post_file.read().strip()
    with open("./photos/horse.jpg", "rb") as photo:
        context.bot.send_photo(
            chat.id,
            photo,
            caption=post_text)


def voice_message_handler(update, context):
    chat = update.effective_chat
    message_voice = update.message.voice
    voice_file_path = context.bot.get_file(message_voice.file_id).file_path
    text = speech_to_text(voice_file_path)
    context.bot.send_message(chat.id, text=f'Распознанный текст:\n "{text}"')
    if text.lower() == "пришли ссылку на блог":
        send_blog_link(update, context)


def send_blog_link(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, text="Высылаю ссылку, как ты просил: https://t.me/kate_groks")


def callback_query_handler(update, context):
    callback_data = update.callback_query.data
    if callback_data == SELFIE_BUTTON_CALLBACK_DATA:
        selfie_command_handler(update, context)
    elif callback_data == SCHOOL_PHOTO_BUTTON_CALLBACK_DATA:
        school_photo_command_handler(update, context)
    elif callback_data == SQL_BUTTON_CALLBACK_DATA:
        sql_command_handler(update, context)
    elif callback_data == GPT_BUTTON_CALLBACK_DATA:
        gpt_command_handler(update, context)
    elif callback_data == LOVE_BUTTON_CALLBACK_DATA:
        love_command_handler(update, context)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('TOKEN')

    bot = Bot(token=token)
    updater = Updater(token=token)

    updater.dispatcher.add_handler(CommandHandler('start', start_command_handler))
    updater.dispatcher.add_handler(CommandHandler('help', help_command_handler))
    updater.dispatcher.add_handler(CommandHandler('git', git_command_handler))
    updater.dispatcher.add_handler(CommandHandler('post', post_command_handler))
    updater.dispatcher.add_handler(CommandHandler('photo', photo_command_handler))
    updater.dispatcher.add_handler(CommandHandler('voice', voice_command_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.voice, voice_message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

    updater.start_polling()
    updater.idle()
