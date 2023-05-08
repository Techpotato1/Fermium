import datetime
import os
import time
from colorama import Fore, Back, Style
from datetime import datetime


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


def calcPi(limit):
    """
    Prints out the digits of PI
    until it reaches the given limit
    """

    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3

    decimal = limit
    counter = 0

    while counter != decimal + 1:
        if 4 * q + r - t < n * t:
            # yield digit
            yield n
            # insert period after first digit
            if counter == 0:
                yield '.'
            # end
            if decimal == counter:
                print('')
                break
            counter += 1
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr
