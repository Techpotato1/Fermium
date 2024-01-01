import os
import platform
import random
from shutil import os
from time import strftime, sleep
import webbrowser
from colorama import Fore, Style
import keyboard
import wikipedia
from requests import get
from getkey import getkey, keys
from datetime import datetime
import configparser

(
    name,
    choice,
    weatherlocation,
    contentsofdir,
    filename,
    ip_address,
    deleteafteruse,
    config
) = (
    "",
    "",
    "",
    os.listdir(os.getcwd()),
    "userinfo.ini",
    get("https://api.ipify.org").text, 
    False, 
    configparser.ConfigParser()
)

print("Loading, please wait...")
options = [
    "What would you like to do next?",
    "1. Check the time",
    "2. Check the date",
    "3. Check the weather (not precise)",
    "4. Clear temp files",
    "5. Wikipedia",
    "6. Settings",
    "7. Exit",
]

# TODO: clear temp files in linux
# remove windows only features
if not os.name == "nt":
    del options[4]

def writetoline(key, data_to_write):
    if not deleteafteruse:
        config["Settings"][key] = data_to_write
        with open(filename, 'w') as configfile:
            config.write(configfile)
            
def readfile(data):
    config.read(filename)
    return config["Settings"][data]

def clearscreen():
    print("\033[2J\033[H", end="", flush=True)

# print color to the terminal
def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function
    but with colors and brightness
    """
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)

def gettime():
    return strftime("%I:%M %p")

# seconds
def gettimespecific():
    return strftime("%I:%M:%S %p")


# calculate pi to a specified limit
# yay yoinking code!
def calcPi(limit):
    """
    Prints out the digits of PI
    until it reaches the given limit
    """

    (q,r,t,k,n,l,) = (1, 0, 1, 1, 3, 3)

    decimal = limit
    counter = 0

    while counter != decimal + 1:
        if 4 * q + r - t < n * t:
            # yield digit
            yield n
            # insert period after first digit
            if counter == 0:
                yield "."
            # end
            if decimal == counter:
                print("")
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


# definitely wrote this, however I did modify substantially
def getweather(temp = False, temp_high = False):
    # HTTP request
    response = get("https://api.openweathermap.org/data/2.5/weather?" + "q=" + weatherlocation + "&units=imperial" + "&appid=" + "9942f72d8fddd917dc980f5d4c6d8b1f")
    # checking the status code of the request
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data["main"]
        # getting temperature
        temperature = int(main["temp"])
        # temp max and min
        mintemp = int(main["temp_min"])
        maxtemp = int(main["temp_max"])
        # getting the humidity
        humidity = main["humidity"]
        # getting the pressure
        pressure = main["pressure"]
        # weather report
        report = data["weather"]
        if temp == True:
            return temperature
        if temp_high == True:
            return maxtemp
        else:
            return f"{weatherlocation:-^32}\nTemperature: {temperature}°F\nHigh/Low: {maxtemp}/{mintemp}°F\nHumidity: {humidity}%\nPressure: {pressure}hPa\nWeather Report: {report[0]['description']}\n{'-' * 32}"
    else:
        # incorrect city
        if weatherlocation == "":
            return "No weather data!"
        else:
            return f"Error in the HTTP request, Status Code: {response.status_code}"

# get the approximate location of the user from their IP address
def getcity():
    url = "https://ip.city/api.php"
    params = {
        "ip": ip_address,
        "key": "e872c03df48ba8d88ee8181e852599ba",
    }
    response = get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response and extract the city field
        data = response.json()
        city = data["city"]
        region = data["region"]
    return (f"{city}, {region}")


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
def getdate():
    return strftime("%A, %B %d, %Y")

# read name
if os.path.exists(filename):
    name = readfile("name")
    weatherlocation = readfile("weather_location")
else:
    config["Settings"] = {"name" : "", "weather_location" : ""}
    with open(filename, 'w') as configfile:
        config.write(configfile)

clearscreen()

# ask for name
# userinfo is created, the code should work if no one tampers with the file
if name == "":
    name = input("What's your name? (shred/incognito to not save any data)\n").capitalize()
    # don't write userinfo
    if name == "Shred" or name == "Incognito":
        deleteafteruse = True
        name = "Anonymous"
        print_with_color("Settings will not be saved!", color=Fore.RED)
    elif len(name) > 50:
        print_with_color("Name is unusually long, prodece with caution", color=Fore.RED)
    writetoline("name", name)

if weatherlocation == "":
    wchoice = input("Would you like to autofill the weather location? (y/n)\n").lower()
    if wchoice == "y" or wchoice == "yes":
        weatherlocation = getcity()
        writetoline("weather_location", weatherlocation)

clearscreen()

# greet user
if random.randint(0, 10) == 0:
    print("Good morning and welcome to the Black Mesa Transit System.")
    print(f"The time is {gettime()}. Current topside temperature is {getweather(True)} degrees with an estimated high of {getweather(False, True)}.\nThe Black Mesa compound is maintained at a pleasant 68 degrees at all times.")
    
else:
    print(f"Hello, {name}!")
    print(f"Today's date is {getdate()}")
    print(f"The time is {gettime()}")

while True:
    print("\n" + "\n".join(options))

    choice = input("Enter your choice: ")
    clearscreen()

    # check the time
    if choice == "1": 
        timeold = ""
        if platform.system() == "Windows":
            while not keyboard.is_pressed("esc"):
                curtime = gettimespecific()
                if not timeold == curtime:
                    timeold = curtime
                    clearscreen()
                    print(f"The time is {timeold} \nPress 'esc' to exit")
        else:
            # this shit better work
            while True:
                if getkey(False) == keys.ESCAPE:
                    print("\n")
                    break
                curtime = gettimespecific()
                if not timeold == curtime:
                    timeold = curtime
                    clearscreen()
                    print(f"The time is {timeold} \nPress 'esc' to exit")

    # check the date
    elif choice == "2":
        # prevent against changing at midnight
        print(strftime("%A, %B %d, %Y"))
    # display weather
    elif choice == "3":
        if weatherlocation == "":
            weatherlocation = input("What is your city? Ex: Sacramento, California \n")
            writetoline("weather_location", weatherlocation)
            print(getweather())
        else:
            print(getweather())
                
    elif choice == "4":
        # specify the paths to the temporary folders
        win_temp_path = 'C:\\Windows\\Temp'
        user_temp_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
        # store file deletion errors to a list
        failed_del = []

        # delete files and folders recursively
        def delete_files_and_folders(folder_path):

            # traverse the folder in reverse order
            for root, dirs, files in os.walk(folder_path, topdown=False):
                # delete files in the current directory
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        failed_del.append(str(e))

                # delete empty directories
                for dir_name in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir_name))
                    except Exception as e:
                        failed_del.append(str(e))

        # initial size of the temp folders
        initial_win_temp_size = sum(os.path.getsize(os.path.join(win_temp_path, f)) for f in os.listdir(win_temp_path) if os.path.isfile(os.path.join(win_temp_path, f)))
        initial_user_temp_size = sum(os.path.getsize(os.path.join(user_temp_path, f)) for f in os.listdir(user_temp_path) if os.path.isfile(os.path.join(user_temp_path, f)))

        # continue deleting files and folders until no more can be deleted
        delete_files_and_folders(win_temp_path)
        delete_files_and_folders(user_temp_path)
        
        # final size of the temp folders
        final_win_temp_size = sum(os.path.getsize(os.path.join(win_temp_path, f)) for f in os.listdir(win_temp_path) if os.path.isfile(os.path.join(win_temp_path, f)))
        final_user_temp_size = sum(os.path.getsize(os.path.join(user_temp_path, f)) for f in os.listdir(user_temp_path) if os.path.isfile(os.path.join(user_temp_path, f)))

        # difference in megabytes
        total_size_difference_mb = ((initial_win_temp_size - final_win_temp_size) + (initial_user_temp_size - final_user_temp_size)) / (1024 * 1024)

        print_with_color(f"{round(total_size_difference_mb, 1)} MB was removed!", color=Fore.GREEN)
        print("It is recommended to run this function with administrator privileges. If you didn't do that, you might not be getting the best results.")
        if input("Would you like to see the undeleted files? (y/n)\n") == "y":
            print("\n".join(failed_del))
        else:
            clearscreen()
            
    # search wikipedia
    elif choice == "5":
        wikipediachoice = ""
        wikipediacount = 3
        while True:
            print("1. Search Wikipedia \n2. Change sentence count \n3. Back")
            wikipediachoice = input("What would you like to do? \n")
            if wikipediachoice == "1":
                try:
                    clearscreen()
                    searchterm = input("Enter a search term: \nUse parentheses to denote the type, ex: Mars (planet) \n")
                    clearscreen()
                    print("Loading!")
                    print(wikipedia.summary(searchterm, sentences=wikipediacount,))
                    print("\n")
                except wikipedia.exceptions.DisambiguationError:
                    print_with_color("Try adding a type to your query.", color=Fore.RED)
                except Exception as e:
                    print(f"Error: {e}", color=Fore.RED)
            elif wikipediachoice == "2":
                try:
                    clearscreen()
                    wikipediacount = int(input("Enter the number of sentences to display: \n"))
                    print_with_color(f"Number of sentences changed to: {wikipediacount}", color=Fore.GREEN)
                except ValueError:
                    print_with_color("Invalid number!", color=Fore.RED)
                    continue
            elif wikipediachoice == "3":
                clearscreen()
                break
            else:
                print_with_color("Invalid choice!", color=Fore.RED)
        
            
    # settings
    elif choice == "6":
        print("1. Change Weather Location \n2. Change Name \n3. Delete info \n4. Autofill weather location from IP \n5. Back")
        setchoice = input("What would you like to do?\n")
        if setchoice == "1":
            clearscreen()
            weatherlocation = input("What is your city? Ex: Sacramento, California\n")
            writetoline("weather_location", weatherlocation)
        elif setchoice == "2":
            clearscreen()
            name = input("What is your name? \n")
            writetoline("name", name)
        elif setchoice == "3":
            try:
                os.remove(filename)
                print_with_color("Deleting user info...", color=Fore.RED)
                print_with_color("Done!", color=Fore.GREEN)
            except Exception as e:
                print_with_color("Failed to delete!", color=Fore.RED)
                print_with_color(f"Error: {e}", color=Fore.RED)
        elif setchoice == "4":
            writetoline("weather_location", getcity())
            clearscreen()
            print(f"Your city is {weatherlocation}.")
            sleep(3)
        clearscreen()
                

    # exit and delete info, if needed
    elif choice == "7":
        os._exit(0)

    elif choice == "69":
        print_with_color("Developer mode activated!", color=Fore.RED)
        clearscreen()
        while choice.lower() != "exit" and choice.lower() != "devexit":
            devops = [
                "8. Clear the screen",
                "10. List the contents of the current directory",
                "12. Open a URL",
                "14. Print your public IP address",
                "15. Generate a random number",
                "16. Calculate PI",
            ]
            print("\n".join(devops))
            choice = input("Enter your choice: ")
            clearscreen()
            if choice == "8":
                print("Clearing screen...")
                clearscreen()

            # list the contents of the current directory
            elif choice == "10":
                print("Contents of the current directory: \n")
                for i in contentsofdir:
                    print(i)
                print("\n")

            # ask the user what url they want to open
            # somewhat broken, website detection is janky
            elif choice == "12":
                urlopen = input("What is the url you want to open? \n")
                webbrowser.open_new("https://" + urlopen)
                pos = urlopen.rfind(".")
                if pos >= 0:
                    urlopen = urlopen[:pos]
                print_with_color(f"Opened {urlopen} in a new tab", color=Fore.GREEN)
                if "e621" in urlopen:
                    print_with_color("You sly dog ;)", color=Fore.GREEN)

            # display IP
            elif choice == "14":
                print(f"Your IP address is {ip_address}.\n")

            # random num
            elif choice == "15":
                firstbetween = int(input("What is the smallest number? \n"))
                secondbetween = int(input("What is the largest number? \n"))
                if firstbetween > secondbetween:
                    print_with_color("The first number must be smaller than the second number. \n", color=Fore.RED)
                else:
                    print(f"Your random number is {str(random.randint(firstbetween, secondbetween))} .\n")
            # calculate pi to a specified amount
            elif choice == "16":
                start = datetime.now()
                try:
                    cpi()
                    print_with_color("Done!", color=Fore.GREEN)
                except KeyboardInterrupt:
                    print_with_color("Canceled!", color=Fore.RED)
                end = datetime.now()
                # format the time difference nicely
                time_difference = end - start
                print(f"Time taken: {str(time_difference)}\n")

    else:
        print_with_color("Invalid choice.", color=Fore.RED)
