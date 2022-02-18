import ctypes


def show_popup(message):
    ctypes.windll.user32.MessageBoxW(0, message, "TeleRAT!", 0x30)
