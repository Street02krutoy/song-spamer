from os import replace
from re import T
import time
import pyperclip
import keyboard

note = "♪ "
badSimvols = [".", ",", ":", ";", "!", "?", "ь", "\n", "-", " "]
hashStrings = ["", "", ""]
hashSong = []

class configProvider(object):
    def __init__(self, patch):
        self.configFile = open(patch, "r", encoding="utf-8")

        values = dict()

        lines = self.configFile.readlines()
        
        for line in lines:
            if not ("#" in line):
                valuesOfString = line.replace("\n", "").split(":")
                
                startPos = valuesOfString[1].find('"')+1
                lastPos = valuesOfString[1].rfind('"')

                if(startPos>-1 and lastPos>-1 and lastPos != startPos):
                    value = valuesOfString[1][startPos:lastPos]
                else:
                    value = valuesOfString[1]

                values[valuesOfString[0]] = value
                
        self.values = values
        
class DiscordModule(object):
    def __init__(self) -> None:
        super().__init__()

    def script(self, st):
        return st

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

    global hashSong, frazaHash
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
    global hashSong, note

    provider = configProvider("Spamerka.config")

    cooldown = int(provider.values.get("Cooldown"))
    note = provider.values.get("NoteSimvol")
    songlist = provider.values.get("Files").split(";")

    print("Начинаю печатать ...")
    for song in songlist:
        print("Start newsong")
        getSongs(song)
    
        time.sleep(5)
    
        for i in hashSong:
            printText(i)
            if cooldown>0: time.sleep(cooldown)

    print("Закончил писать ...")

Main()
