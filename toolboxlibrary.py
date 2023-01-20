from base64 import decode
import datetime
import os
import random
import shutil
import time
import webbrowser
import requests
import json
from requests import get
import pyttsx3
from colorama import init, Fore, Back, Style
from datetime import datetime
import keyboard
import wikipedia
import sys

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)

FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
         Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
# all available background colors
BACKS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW,
         Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
# brightness values
BRIGHTNESS = [Style.DIM, Style.NORMAL, Style.BRIGHT]

#get the time and format it nicely
def gettime():
    currenttime = datetime.now()
    currenttime = time.strftime("%I:%M %p")
    return currenttime

#get the time with seconds
def gettimespecific():
    currenttime = datetime.now()
    currenttime = time.strftime("%I:%M:%S %p")
    return currenttime
