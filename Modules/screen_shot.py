# Program to take a screenshot of the screen
import pyautogui


def screen_shot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r"screenshot.png")
