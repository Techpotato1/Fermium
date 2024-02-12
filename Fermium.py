import configparser
import os
import platform
import random
from shutil import os
from time import strftime, sleep
from rich import print
import keyboard
import wikipedia
from requests import get
from getkey import getkey, keys
import argparse

name = ""
choice = ""
weatherlocation = ""
filename = "userinfo.ini"
ip_address = get("https://api.ipify.org").text
config = configparser.ConfigParser()

# get cmd arguments 
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--noauto', action='store_true', help='turn off the autofill of certain data')
parser.add_argument('-p', '--portable', action='store_true', help='don\'t store data')
parser.add_argument('-d', '--delete', action='store_true', help='delete previous data before running')
args = parser.parse_args()

if args.delete:
    try:
        os.remove(filename)
    except FileNotFoundError:
        print("[red]No userfile detected![/red]")

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
    if not args.portable:
        config["Settings"][key] = data_to_write
        with open(filename, 'w') as configfile:
            config.write(configfile)
            
def readfile(data):
    config.read(filename)
    return config["Settings"][data]

def clearscreen():
    print("\033c", end="", flush=True)

def gettime():
    return strftime("%I:%M %p")

# seconds
def gettimespecific():
    return strftime("%I:%M:%S %p")

# definitely wrote this
# however I did modify substantially
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
            return f"{weatherlocation:-^32}\nTemperature: {temperature}°F\nHigh/Low: {maxtemp}/{mintemp}°F\nHumidity: {humidity}%\nPressure: {pressure}hPa\nWeather Report: {str(report[0]['description']).capitalize()}\n{'-' * 32}"
    else:
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
    try:
        response = get(url, params=params)
    except:
        print(f"Error in the HTTP request, Status Code: {response.status_code}")

    # check if the request was successful (status code 200)
    if response.status_code == 200:
        # parse the JSON response and extract the city field
        data = response.json()
        city = data["city"]
        region = data["region"]
    return (f"{city}, {region}")

# format the date nicely
def getdate():
    # add date ordinals
    nice_dateday = strftime("%#d")
    if nice_dateday[-1] == "1":
        nice_dateday +="st"
    elif nice_dateday[-1] == "2":
        nice_dateday +="nd"
    elif nice_dateday[-1] == "3":
        nice_dateday +="rd"
    else:
        nice_dateday +="th"
    nice_date = strftime(f"%A, %B {nice_dateday}, %Y")
    return nice_date

# read data from config 
if os.path.exists(filename):
    name = readfile("name")
    weatherlocation = readfile("weather_location")
elif not args.portable:
    config["Settings"] = {"name" : "", "weather_location" : ""}
    with open(filename, 'w') as configfile:
        config.write(configfile)

clearscreen()

# get user's info, unless portable
# !!!userinfo is created!!!
if name == "":
    # don't write to file
    if args.portable:
        name = "Anonymous"
        print("[red]Settings will not be saved![/red]")
    else:
        name = input("What's your name? (running with -p flag does't save data)\n").title()
        writetoline("name", name)
        if args.noauto == False:  
            weatherlocation = getcity()
            writetoline("weather_location", weatherlocation)
        else:
            if input("Would you like to autofill the weather location? (y/n)\n").lower() == "y" or "yes":
                weatherlocation = getcity()
                writetoline("weather_location", weatherlocation)

clearscreen()

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

    # display the date
    elif choice == "2":
        print(getdate())
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

        print(f"[green]{round(total_size_difference_mb, 1)} MB was removed![/green]")
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
                    # not specific enough 
                    print("[red]Try adding a type to your query.[/red]")
                except Exception as e:
                    print(f"[red]Error:[/red] {e}")
            elif wikipediachoice == "2":
                try:
                    clearscreen()
                    wikipediacount = int(input("Enter the number of sentences to display: \n"))
                    print(f"[red]Number of sentences changed to: {wikipediacount}[/red]")
                except ValueError:
                    print("[red]Invalid number![/red]")
                    continue
            elif wikipediachoice == "3":
                clearscreen()
                break
            else:
                print("[red]Invalid choice![/red]")
        
            
    # user settings
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
            # remove config
            try:
                os.remove(filename)
                print("[red]Deleting user info...[/red]")
                print("[red]Done![/red]")
            except Exception as e:
                print("[red]Failed to delete![/red]")
                print(f"[red]Error:[/red] {e}")
        elif setchoice == "4":
            writetoline("weather_location", getcity())
            clearscreen()
            print(f"Your city is {getcity()}.")
            sleep(3)
        clearscreen()          
    # exit
    elif choice == "7":
        os._exit(0)
        
    else:
        print("[red]Invalid choice.[/red]")
