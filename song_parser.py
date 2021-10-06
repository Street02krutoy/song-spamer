from os import replace
from re import T
import time
import pyperclip
import keyboard
from config import settings

# Minecraft Module
note = "♪ "
badSimvols = [".", ",", ":", ";", "!", "?", "ь", "\n", "-", " "]
hashStrings = ["", "", ""]
hashSong = []
if not settings["slowmode"] == 0:
    timeToSleep = settings["slowmode"] + 2
else:
    timeToSleep = settings["no-slowmode"]


class DiscordModule(object):
    def __init__(self) -> None:
        super().__init__()

    def script(self, st):
        return st


class MinecraftModule(object):
    mode_global = True

    def __init__(self, mode_global):
        self.mode_global = mode_global

    def script():
        keyboard.press_and_release("t")
        time.sleep(0.1)
        keyboard.press_and_release("shift + 1")


def printText(text):
    pyperclip.copy(text)
    keyboard.press_and_release("ctrl + v")
    time.sleep(0.01)
    keyboard.press_and_release("enter")


def getFirstEmpity():
    global hashStrings
    flag = 0
    for i in hashStrings:
        if i == "":
            return flag
        flag += 1
    return flag + 1


def isRifma(arg1, arg2):
    if arg1 == arg2:
        return True
    elif (arg1 == "д" or arg1 == "т") and (arg2 == "д" or arg2 == "т"):
        return True
    elif (arg1 == "с" or arg1 == "з") and (arg2 == "с" or arg2 == "з"):
        return True
    else:
        return False


def removeVadSimvols(text):
    global badSimvols
    for badSimvol in badSimvols:
        text = text.replace(badSimvol, "")
    return text


def checkRifma(text):
    global hashStrings
    text = removeVadSimvols(text)[-1:]
    if isRifma(hashStrings[2], text) or isRifma(hashStrings[1], text):
        hashStrings = ["", "", ""]
        return True
    hashStrings = [hashStrings[1], hashStrings[2], text]
    return False


frazaHash = ""


def getSongs(patch):
    file = open(patch, "r", encoding="utf-8")
    strings = file.readlines()
    file.close()

    global hashSong
    global frazaHash
    flag = 0
    for i in strings:
        if checkRifma(i):
            i = i + note
        frazaHash = frazaHash + i
        flag += 1
        if flag > 3:
            hashSong.append(frazaHash)
            frazaHash = ""
            flag = 0


def Main():
    global hashSong, timeToSleep
    getSongs(settings["file"])
    print("Начинаю печатать ...")
    time.sleep(settings["start-latency"])
    for i in hashSong:
        printText(i)
        time.sleep(timeToSleep)
    print("Закончил писать")


Main()
