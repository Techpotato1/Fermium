import datetime
import os
import platform
import random
from shutil import os
from time import strftime
import webbrowser
from colorama import Fore, Back, Style
import keyboard
import wikipedia
from requests import get
from getkey import getkey, keys
from datetime import datetime

name, choice, weatherlocation, wikipediacount, wikipediachoice, contentsofdir = "", "", "", 3, "", os.listdir(os.getcwd())

print("Loading, please wait...")
options = ["What would you like to do next?", "1. Check the time", "2. Check the date", "3. Check the weather", "4. Wikipedia", "5. Settings", "6. Exit"]

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# print color to the terminal
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

def gettime():
    currenttime = strftime("%I:%M %p")
    return currenttime

# seconds
def gettimespecific():
    currenttime = strftime("%I:%M:%S %p")
    return currenttime

# calculate pi to a specified limit
# yay yoinking code!
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

# definitely wrote this
def getweather():
    # base URL
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    # City Name
    CITY = weatherlocation
    # updating the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + "9942f72d8fddd917dc980f5d4c6d8b1f"
    # HTTP request
    response = get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data["main"]
        # getting temperature
        temperature = main["temp"]
        # getting the humidity
        humidity = main["humidity"]
        # getting the pressure
        pressure = main["pressure"]
        # weather report
        report = data["weather"]
        # convert the temperature to fahrenheit
        temperature = temperature * (9 / 5) - 459.67
        # round the temperature to 2 decimal places
        temperature = round(temperature)
        print(f"{CITY:-^30}")
        print(f"Temperature: {temperature}°f")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure}hPa")
        print(f"Weather Report: {report[0]['description']}")
    else:
        # showing the error message
        print_with_color(
            "Error in the HTTP request", color=Fore.RED
        )
        print("Try checking the city name")
        
ip_address = get("https://api.ipify.org").text

# get the approximate location of the user from their IP address
def getcity():
    url = 'https://ip.city/api.php'
    params = {
        'ip': ip_address,
        'key': 'e872c03df48ba8d88ee8181e852599ba'
    }
    response = get(url, params=params)

    #Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response and extract the city field
        data = response.json()
        city = data['city']
        region = data['region']
    return city + ", " + region


# Wrapper function for calculating pi
def cpi():
    # Calls CalcPi with the given limit
    pi_digits = calcPi(int(input("Enter the number of decimals to calculate to: ")))

    i = 0

    # Prints the output of calcPi generator function
    # Inserts a newline after every 40th number
    for d in pi_digits:
        print(d, end="")
        i += 1
        if i == 40:
            print("")
            i = 0

# format the date nicely
date = strftime("%A, %B %d, %Y")
currenttime = gettime()

# read name
try:
    with open("userinfo.txt", "r", encoding="utf-8") as f:
            name = f.readline().strip()
except FileNotFoundError:
        pass
    
# read weatherlocation
try:
    with open("userinfo.txt", "r") as f:
        # Skip the first line
        f.readline()
        # Read the second line
        weatherlocation = f.readline().strip()
except:
    pass

deleteafteruse = False

clearscreen()

# ask for name
# userinfo is created, the code should work if no one tampers with the file
if name == "":
    name = input("What is your name? \n")
    name = name.capitalize()
    try:
        with open("userinfo.txt", "w") as f:
            nameencoded = name.encode("utf-8", "strict")
            f.write(name)
    except Exception as e:
        print_with_color("Error creating file!", color=Fore.RED)
        print_with_color(
            "This may cause errors in several functions!",
            color=Fore.RED,
        )
        print(f"{e}")

# don't store user info
if(name.lower() == "shred" or name.lower() == "incognito"):
    deleteafteruse = True
    name = "Anonymous"
    print_with_color("Incognito mode activated!", color=Fore.RED)
    
if weatherlocation == "":
    wchoice = input("Would you like to autofill the weather location? \n")
    if wchoice == "y" or wchoice == "yes":
        weatherlocation = getcity()
        with open("userinfo.txt", "r+") as f:
            # again this is stupid
            f.readline()
            f.write("".join(["\n", weatherlocation]))
    else:
        # dumb solution but works
        weatherlocation = ""

clearscreen()
# greet user

print("".join(["Hello, ", name, "!"]))
print("".join(["Today's date is ", date]))
print("".join(["The time is ", currenttime, "\n"]))
while choice != "6":
    print('\n'.join(options))

    choice = input("Enter your choice: ")
    
    clearscreen()

    
# check the time
    if choice == "1" or choice == "time":
        timeold = ""
        if platform.system() == "Windows":
            while not keyboard.is_pressed("esc"):
                curtime = gettimespecific()
                if not timeold == curtime:
                    timeold = curtime
                    clearscreen()
                    print("".join(["The time is ", timeold, "\nPress 'esc' to exit"]))
        else:
            # this shit better work
            while True:
                if getkey(False) == keys.ESCAPE:
                    break
                curtime = gettimespecific()
                if not timeold == curtime:
                    timeold = curtime
                    clearscreen()
                    print("".join(["The time is ", timeold, "\nPress 'esc' to exit"]))

    # check the date
    elif choice == "2" or choice == "date":
        print(date)
    # display weather
    elif choice == "3" or choice == "weather":
        if weatherlocation == "":
            weatherlocation = input("What is your city? (Zip codes will work) \n")
            with open("userinfo.txt", "r+") as f:
                f.readline()
                f.write("".join(["\n", weatherlocation]))
            getweather()
            print('\n')
        else:
            getweather()
            print('\n')

    # change name
    

    elif choice == "4" or choice == "wikipedia":
        while(wikipediachoice != "3"):
            print("1. Search Wikipedia \n2. Change sentence count \n3. Back")
            wikipediachoice = input("What would you like to do? \n")
            if wikipediachoice == "1":
                try:
                    clearscreen()
                    searchterm = input(
                        "Enter a search term: \n(Use parentheses to denote the type, ex: Mars (planet) \n"
                    )
                    clearscreen()
                    print("Loading!")
                    print(wikipedia.summary(searchterm, sentences=wikipediacount))
                    print("\n")
                except wikipedia.exceptions.DisambiguationError:
                    print_with_color("Invalid Search Term!", color=Fore.RED)
                    print_with_color("Try again!", color=Fore.RED)
                except:
                    print_with_color("Unexpected error!", color=Fore.RED)
            elif wikipediachoice == "2":
                try:
                    clearscreen()
                    wikipediacount = int(
                        input("Enter the number of sentences to display: \n")
                    )
                    print_with_color(
                        "".join(["Number of sentences changed to: ",str(wikipediacount)]),
                        color=Fore.GREEN,
                    )
                except:
                    print_with_color("Invalid Number!", color=Fore.RED)
            elif wikipediachoice == "3":
                pass
            else:
                print_with_color("Invalid number!", color=Fore.RED)
    elif choice == "5" or choice.lower() == "settings":
        print("1. Change Weather Location \n2. Change Name \n3. Exit")
        setchoice = input("What would you like to do?\n")
        if setchoice == "1":
            weatherlocation = input("What is your city? \n")
            with open("userinfo.txt", "w") as f:
                f.readline()
                f.write("".join(["\n", weatherlocation]))
        elif setchoice == "2":
            name = input("What is your name? \n")
            # prevent unreadable text due to long names
            if(len(name) > 1000):
                print_with_color("Name is too long!", color=Fore.RED)
                pass
            try:
                with open("userinfo.txt", "w") as f:
                    f.write(name)
                print_with_color("".join(["Name Changed to: ", name]), color=Fore.GREEN)
            except:
                print_with_color("Invalid Name!", color=Fore.RED)
    
    # exit and delete info, if needed
    elif choice == "6" or choice == "exit":
        if(deleteafteruse):
            try:
                os.remove("userinfo.txt")
                print_with_color(
                    "Deleting user info...", color=Fore.RED, 
                )
                print_with_color("Done!", color=Fore.GREEN)
            except:
                    print_with_color("Some files failed to delete", color=Fore.RED,)
                    pass
        clearscreen()
        try:
            exit()
        except:
            os._exit(0)
            
    elif choice == "69" or choice.lower() =="dev":
        print_with_color("Developer mode activated!", color=Fore.RED)
        clearscreen()
        while choice.lower() != "exit" and choice.lower() != "devexit":
            devops = ['8. Clear the screen', '9. Delete the user info', '10. List the contents of the current directory', '12. Open a URL', '13. Autofill the weather location from IP', '14. Print your public IP address', '15. Generate a random number', '16. Calculate PI']
            print('\n'.join(devops))
            choice = input("Enter your choice: ")
            clearscreen()
            if choice == "8" or choice == "clear":
                print("Clearing screen...")
                clearscreen()

            # delete userinfo
            elif choice == "9" or choice == "delete info":
                try:
                    os.remove("userinfo.txt")
                    print_with_color(
                        "Deleting user info...", color=Fore.RED, 
                    )
                    print_with_color("Done!", color=Fore.GREEN)
                except:
                    print_with_color(
                        "Some files failed to delete", color=Fore.RED, 
                    )
                    pass

            # list the contents of the current directory
            elif choice == "10" or choice == "list current dir":
                print("Contents of the current directory: \n")
                for i in contentsofdir:
                    print(i)
                print("\n")

            # ask the user what url they want to open
            # somewhat broken, website detection is janky
            elif choice == "12" or choice == "open url":
                urlopen = input("What is the url you want to open? \n")
                webbrowser.open_new("https://" + urlopen)
                pos = urlopen.rfind('.')
                if pos >= 0:
                    urlopen = urlopen[:pos]
                #TODO: Implement default browser detection
                print_with_color("".join(["Opened ", urlopen.capitalize(), " in a new tab"]), color=Fore.GREEN) 

            # update location with ip
            # works as long as you don't fuck with the file
            # breaks if user changes their name
            elif choice == "13" or choice == "ip locate":
                weatherlocation = getcity()
                with open("userinfo.txt", "r") as f:
                    wdata = f.readlines()
                    wdata[1] = weatherlocation
                with open("userinfo.txt", "w") as f:
                    f.writelines(wdata)
                print("".join(["Your city is ", weatherlocation, ".\n"]))

            # display IP
            elif choice == "14" or choice == "ip":
                print("".join(["Your IP address is ", ip_address, ".\n"]))

            # random num
            elif choice == "15" or choice == "randomnum":
                firstbetween = int(input("What is the smallest number? \n"))
                secondbetween = int(input("What is the largest number? \n"))
                if firstbetween > secondbetween:
                    print_with_color(
                        "The first number must be smaller than the second number. \n",
                        color=Fore.RED,
                    )
                else:
                    print("".join(["Your random number is ", str(random.randint(firstbetween, secondbetween)), ".\n"]))
            # calculate pi to a specified amount
            elif choice == "16" or choice == "pi":
                start = datetime.now()
                try:
                    cpi()
                    print_with_color("Done!", color=Fore.GREEN)
                except KeyboardInterrupt:
                    print_with_color("Canceled!", color=Fore.RED)
                    pass
                end = datetime.now()
                # format the time difference nicely
                time_difference = end - start
                print("".join(["Time taken: ", str(time_difference), "\n"]))

    else:
        print_with_color(
            "Invalid choice.\n", color=Fore.RED
        )
