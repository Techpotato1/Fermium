import datetime
import os
import platform
import random
import shutil
import time
import webbrowser
from colorama import init, Fore, Back, Style
import keyboard
import wikipedia
from requests import get
import sys
from getkey import getkey, keys
from datetime import datetime

# essential for Windows environment
if os.name == 'nt':
    init()

# print the the options for the user to choose from
def printoptions():
    print(
        """What would you like to do next? \n
1. Check the time
2. Check the date
3. Change the weather location
4. Check the weather
5. Change your name
6. Wikipedia
7. Exit \n
"""
    )

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# define a method for printing color to the terminal
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
    currenttime = time.strftime("%I:%M %p")
    return currenttime

#get the time with seconds
def gettimespecific():
    currenttime = time.strftime("%I:%M:%S %p")
    return currenttime

# calculate pi to a specified limit
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

# get the weather from the API
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


# Create a folder in the same directory as the script called "info"
try:
    os.mkdir("info")
except FileExistsError:
    pass

# Gets the IP address of the user
name = ""
choice = ""
weatherlocation = ""
oldtimeanddate = ""
wikipediacount = 3
wikipediachoice = "0"

# Get the contents of the current directory
contentsofdir = os.listdir(os.getcwd())
contentsofinfodir = os.listdir("info")

# format the date nicely
date = time.strftime("%A, %B %d, %Y")

# setts the currenttime variable to the current time
currenttime = gettime()

# if userinfo.txt exists, open it and read the name
try:
    with open("info/userinfo.txt", "rb") as f:
        nameencoded = f.read()
        name = nameencoded.decode("utf-8", "strict")
except:
    pass

# if weatherlocation.txt exists, open it and read the file
try:
    with open("info/weatherlocation.txt", "r") as f:
        weatherlocation = f.read()
except FileNotFoundError:
    pass

# an unused function to get the last contents of the info folder
try:
    with open("info/currentdir", "r") as f:
        olddircontents = f.read()
except FileNotFoundError:
    pass

# if timeanddate.txt exists, open it and read the file
try:
    with open("info/timeanddate.txt", "r") as f:
        oldtimeanddate = f.read()
except FileNotFoundError:
    pass

# write the time and date to a file called timeanddate.txt
with open("info/timeanddate.txt", "w") as f:
    f.write("Date last run: \n")
    f.write(date)
    f.write("\n")
    f.write(currenttime)

clearscreen()

# if there is nothing in name, ask for it
if name == "":
    name = input("What is your name? \n")
    
if weatherlocation == "":
    if input("Would you like to autofill the weather location? \n") == "yes" or "y":
        weatherlocation = getcity()
        with open("info/weatherlocation.txt", "w") as file:
                file.write(weatherlocation)
    else:
        pass

# create a file called userinfo.txt and write the name to it
try:
    with open("info/userinfo.txt", "wb") as file:
        nameencoded = name.encode("utf-8", "strict")
        file.write(nameencoded)
except:
    print_with_color("Error creating file!", color=Fore.RED)
    print_with_color(
        "You will be asked for your name the next time you open the program.",
        color=Fore.RED,
    )

clearscreen()
# get the user's name and greet them
print("Hello, " + name + "!")
print("Today's date is " + date)
print("The time is " + currenttime)

# Don't exit the program until the user enters 7
while choice != "7":
    printoptions()

    choice = input("Enter your choice: ")
    
    clearscreen()

    
# if the user chooses 1, check the time
    if choice == "1" or choice == "time":
        timeold = ""
        if platform.system() == "Windows":
            while not keyboard.is_pressed("esc"):
                curtime = gettimespecific()
                if not timeold == curtime:
                    timeold = curtime
                    clearscreen()
                    print("The time is " + timeold + "\nPress 'esc' to exit")
        else:
            # this shit better work
            while True:
                if getkey(False) == keys.ESCAPE:
                    break
                curtime = gettimespecific()
                if not timeold == curtime:
                    timeold = curtime
                    clearscreen()
                    print("The time is " + timeold + "\nPress 'esc' to exit")

    # if the user chooses 2, check the date
    elif choice == "2" or choice == "date":
        print(date)

    # if the user chooses 3, get the weather location
    elif choice == "3":
        weatherlocation = input("What is your city? \n")
        with open("info/weatherlocation.txt", "w") as file:
            file.write(weatherlocation)

    # if the user chooses 4, get the weather
    elif choice == "4" or choice == "weather":
        if weatherlocation == "":
            weatherlocation = input("What is your city? (Zip codes will work) \n")
            with open("info/weatherlocation.txt", "w") as file:
                file.write(weatherlocation)
            getweather()
            print("\n")
        else:
            getweather()
            print("\n")

    # if the user chooses 5, get the user's name
    elif choice == "5" or choice == "name":
        name = input("What is your name? \n")
        if(len(name) > 1000):
            print_with_color("Invalid Name!", color=Fore.RED)
            pass
        try:
            with open("info/userinfo.txt", "w") as file:
                file.write(name)
            print_with_color("Name Changed to: " + name, color=Fore.GREEN)
        except:
            print_with_color("Invalid Name!", color=Fore.RED)

    elif choice == "6" or choice == "wikipedia":
        print("1. Search Wikipedia \n" + "2. Change sentence count")
        wikipediachoice = input("What would you like to do \n")
        if wikipediachoice == "1":
            try:
                clearscreen()
                searchterm = input(
                    "Enter a search term: \n"
                    + '(Use parentheses to denote the type, ex: "Mars (Planet)") \n'
                )
                clearscreen()
                print("Loading!")
                print(wikipedia.summary(searchterm, sentences=wikipediacount))
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
                    "Number of sentences changed to: " + str(wikipediacount),
                    color=Fore.GREEN,
                )
            except:
                print_with_color("Invalid Number!", color=Fore.RED)
        else:
            print_with_color("Invalid number!", color=Fore.RED)

    # if the user chooses 7, exit the program
    elif choice == "7" or choice == "exit":
        clearscreen()
        try:
            sys.exit()
        except:
            os._exit(0)
            
    elif choice == "69":
        print_with_color(
            "Developer mode activated!", color=Fore.RED
        )
        time.sleep(1)
        clearscreen()
        while choice != "devexit":
            time.sleep(2)
            print(
                """Developer Options:
8. Clear the screen
9. Delete the info folder
10. List the contents of the current directory
11. Check the time that the program was last run
12. Open a URL
13. Autofill the weather location from IP
14. Print your public IP address
15. List the contents of the info folder
16. Generate a random number
17. Calculate PI
Devexit"""
            )
            choice = input("Enter your choice: ")
            clearscreen()
            if choice == "8" or choice == "clear":
                print("Clearing screen...")
                time.sleep(0.5)
                clearscreen()

            # if the user chooses 9, delete the info folder
            elif choice == "9" or choice == "delete info":
                try:
                    shutil.rmtree("info")
                    print_with_color(
                        "Deleting info folder...", color=Fore.RED, 
                    )
                    time.sleep(0.5)
                    print_with_color("Done!", color=Fore.GREEN)
                except:
                    print_with_color(
                        "Some files failed to delete", color=Fore.RED, 
                    )
                    pass

            # if the user chooses 10, list the contents of the current directory
            elif choice == "10" or choice == "list current dir":
                print("Contents of the current directory: \n")
                for i in contentsofdir:
                    print(i)
                print("\n")

            # if the user chooses 11, display the time the program was last run
            elif choice == "11" or choice == "time last run":
                if oldtimeanddate == "":
                    print("No previous time and date")
                else:
                    print(oldtimeanddate)

            # if the user chooses 12, ask the user what url they want to open
            elif choice == "12" or choice == "open url":
                # ask the user what url they want to open
                urlopen = input("What is the url you want to open? \n")
                # open the url in the default browser
                webbrowser.open_new(urlopen)

            # if the user chooses 13, locate their current location using their IP address
            elif choice == "13" or choice == "ip locate":
                weatherlocation = getcity()
                with open("info/weatherlocation.txt", "w") as file:
                    file.write(weatherlocation)
                print("Your city is " + weatherlocation + "." + "\n")

            # if the user chooses 13, display their current IP address
            elif choice == "14" or choice == "ip":
                print("Your IP address is " + ip_address + "." + "\n")

            # if the user chooses 15, display contents of the info folder
            elif choice == "15" or choice == "list info":
                print("Contents of the info directory: \n")
                contentsofinfodir = os.listdir("info")
                for i in contentsofinfodir:
                    print(i)
                print("\n")

            # if the user chooses 16, choose a random number
            elif choice == "16" or choice == "randomnum":
                firstbetween = int(input("What is the smallest number? \n"))
                secondbetween = int(input("What is the largest number? \n"))
                if firstbetween > secondbetween:
                    print_with_color(
                        "The first number must be smaller than the second number. \n",
                        color=Fore.RED,
                    )
                else:
                    print(
                        "Your random number is "
                        + str(random.randint(firstbetween, secondbetween))
                        + "."
                        + "\n"
                    )
            # if the user chooses 17, calculate pi to the specified amount
            elif choice == "17" or choice == "pi":
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
                print("Time taken: " + str(time_difference) + "\n")

    else:
        print_with_color(
            "Invalid choice." + "\n", color=Fore.RED
        )
