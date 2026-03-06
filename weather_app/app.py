import requests
import sys
import csv
import json
from datetime import datetime
import os
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from collections import deque
from cleaner import clean #function from cleaner.py 


class Collect_data():

    
    def __init__(self, city, temp, windspeed, date):

        self.city = city
        self.temp = temp
        self.windspeed = windspeed
        self.date = date


    def turn_dict(self):

        return {
            'city': self.city,
            'temperature': self.temp,
            'windspeed': self.windspeed,
            'date-time': self.date
        }


WEEK = [
    'Monday','Tuesday','Wednesday',
    'Thursday','Friday','Saturday',
    'Sunday'
]

MONTHS = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May','06': 'Jun', '07': 'Jul','08': 'Aug',
        '09': 'Sep','10': 'Oct','11': 'Nov','12': 'Dec'
}



def forecast():

    while True:

        c = input('Enter the city/country name: ').lower()
        api_1 = f'https://geocoding-api.open-meteo.com/v1/search?name={c}'
        if c == 'q' or c == 'quit':
            sys.exit('Successfully quit!')

        try:

            r = requests.get(api_1)
            j = r.json()

            try:

                if not j['results']:
                    sys.exit("City not found. Check the spelling please!")
                for index, i in enumerate(j['results']):#list all the available cities/countries with the given name
                    print(f"{index+1}){i['name']}, {i['country']}")

            except KeyError:

                print('Invalid city/country name!')
                continue
    

            while True:

                try:

                    user = input("Enter the number of the intended city/country: ").lower()
                    if int(user) < 1 or int(user) > len(j['results']):#if the user chooses a number that does not match the index start the loop again

                        print('Input out of range!')
                        continue
                    
                    break

                except ValueError:

                    if user == "quit": sys.exit('You successfully quit the program!')
                    else:
                        print("Invalid input!")
                        continue


            longitude = j['results'][int(user) - 1]['longitude']#if the user chooses a number it subtract one to match everything (1 == 0, 2 == 1 and etc.)
            latitude = j['results'][int(user) -1]['latitude']
            api3 = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto"


            r2 = requests.get(api3)
            j2 = r2.json()
            units = j2['daily']
            ind = range(1,8)
            maxt = units['temperature_2m_max']#highest temperature
            mint = units['temperature_2m_min']#lowest temperature


            tf = TimezoneFinder()
            zone = tf.timezone_at(
                lng=longitude,
                lat=latitude
            )


            current = datetime.now(ZoneInfo(zone))
            day = current.strftime('%A')#finding the day of the week with a given city/country name

            ind_day = [inde for inde,i in enumerate(WEEK) if i == day][0]#[0] at the end cuz inde returns a list and to extract a value from it we just specify the item we want    
            dates = j2['daily']['time'] 


            dict_ = {
                '01': 'st', '02': 'nd', '03': 'rd'
            }
            for k in range(4,32):
                if k < 10: dict_[f'0{k}'] = 'th'
                dict_[f'{k}'] = 'th' #this is same as appending in a list


            print(f'{'-'*14}\n{'Highest-Lowest'}\n{'-'*14}')
            

            for z,i,x,y,t in zip(ind,maxt, mint, range(7), dates):

                month = MONTHS[str(t[5:7])]
                day = t[8:10]

                y = (ind_day+y)%7#the remainder is the day of the week in sequence, if it is wednesday the ind_day is 3 and it will be added 0 first and wednesday will be given, then 1 will be added and index 4 and thursday
                if 0 < i < 10.0: i = f"0{i}"
                if 0 < x < 10.0: x = f"0{x}"


                print(f'{z}){i}°C|{x}°C||{month} {day}{dict_[day]} |{WEEK[y]}')


            print(f'{'-'*24}\n{'Highest-Lowest (average)'}\n{'-'*24}')
            avg = f"{round(sum(maxt)/len(maxt), 1)}°C|{round(sum(mint)/len(mint), 1)}°C"

            sys.exit(avg)
        except (requests.exceptions.RequestException):
            sys.exit('Connection error!')





                    
def get_country():
    c = " ".join(sys.argv[1:]).lower()
    api_1 = f'https://geocoding-api.open-meteo.com/v1/search?name={c}'
    try:
        r = requests.get(api_1)
        j = r.json()

        if not j['results']:
            sys.exit("City not found. Check the spelling please!")


        for index, i in enumerate(j['results']):
            print(f"{index+1}){i['name']}, {i['country']}")


        while True:
            try:
                user = input("Enter the number of the intended city/country: ").lower()
                if int(user) < 1 or int(user) > len(j['results']):
                    print('Input out of range!')
                    continue
                break
            except ValueError:
                if user == "quit":
                    sys.exit('You successfully quit the program!')
                else:
                    print('Invalid input!')
                    continue


        longitude = j['results'][int(user) - 1]['longitude']
        latitude = j['results'][int(user) -1]['latitude']
        api_2 = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'


        r_2 = requests.get(api_2)
        j_2 = r_2.json()


        j2 = j_2['current_weather']
        temp = j2['temperature']
        w_S = j2['windspeed']
        day = j2['is_day']
        date = j2['time']
        
        l = '-'*26
        print(f"{l}\nThe temperature is {temp}°C")
        print(f"The windspeed is {w_S} km/h")

        if day == 1: print(f'Day time\n{l}')
        else: print(f'Night time\n{l}')


        with open('kregg.csv', 'a', newline='') as f:
            columns = ['city', 'temperature', 'windspeed' ,'date-time']
            writer = csv.DictWriter(f, fieldnames=columns)
            form = Collect_data(c, temp, w_S, date)
            writer.writerow(form.turn_dict())


    except requests.exceptions.RequestException:
        print("Check your connection sir!")
    except(KeyError, ValueError):
        print('City/country not found check the spelling!')



def days(directory, num_of_days, c_name):#an average temperature and windspeed calculator in a given number of searches from the user input
    nm = []
    tem = []
    w__s = []

    with open(directory) as f:

        reader = csv.DictReader(f)
        for i in reader:
            if i['city'] == c_name:
                nm.append(i)

        last_lines = deque(nm, maxlen=num_of_days)
        for x in last_lines:
            temp = x['temperature']
            ws = x['windspeed']
            tem.append(float(temp))
            w__s.append(float(ws))


        avgt = sum(tem)/len(tem)
        avgw = sum(w__s)/len(w__s)
        last_days = len(nm)

        if num_of_days > last_days: raise ValueError#if the user input is higher than the available number of searches in csv it will raise a ValueError
        else: pass
        
        if num_of_days > 1: print(f'{'-'*31}\nNumber of searches: {num_of_days} searches\nTemperature: {round(avgt,1)}°C (average)\nWindspeed: {round(avgw,1)} km/h (average)\n{'-'*31}')
        else: print(f'{'.'*29}\nNumber of searches: {num_of_days} search\nTemperature: {round(avgt,1)}°C\nWindspeed: {round(avgw,1)} km/h\n{'.'*29}')


def set_week():

    while True:
        c = input('Enter the city/country name: ').lower()
        api_1 = f'https://geocoding-api.open-meteo.com/v1/search?name={c}'
        if c == 'q' or c == 'quit':
            sys.exit('Successfully quit!')

        try:

            r = requests.get(api_1)
            j = r.json()

            try:

                if not j['results']:
                    sys.exit("City not found. Check the spelling please!")
                for index, i in enumerate(j['results']):#list all the available cities/countries with the given name
                    print(f"{index+1}){i['name']}, {i['country']}")

            except KeyError:

                print('Invalid city/country name!')
                continue
    

            while True:

                try:

                    user = input("Enter the number of the intended city/country: ").lower()
                    if int(user) < 1 or int(user) > len(j['results']):#if the user chooses a number that does not match the index start the loop again

                        print('Input out of range!')
                        continue
                    
                    break

                except ValueError:

                    if user == "quit": sys.exit('You successfully quit the program!')
                    else:
                        print("Invalid input!")
                        continue




            longitude = j['results'][int(user) - 1]['longitude']#if the user chooses a number it subtract one to match everything (1 == 0, 2 == 1 and etc.)
            latitude = j['results'][int(user) -1]['latitude']
            api3 = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&past_days=7&timezone=auto"
            r = requests.get(api3)
            j = r.json()

            tf = TimezoneFinder()
            zone = tf.timezone_at(
                lng=longitude,
                lat=latitude
            )

            current = datetime.now(ZoneInfo(zone))
            day = current.strftime('%A')#finding the day of the week with a given city/country name

            inde = [inde for inde,h in enumerate(WEEK) if h == day][0]
            maxt = j['daily']['temperature_2m_max']
            mint = j['daily']['temperature_2m_min']
            max_lst = []
            min_lst = []


            y = len(WEEK[0:inde])

            if os.path.getsize('weekly.json') == 0:

                dict_ = {}
                for x,y,z in zip(maxt[7-y:7+(7-y)], mint[7-y:7+(7-y)], range(len(WEEK))):

                    if WEEK[z] == day: dict_[WEEK[z]] = {'max': x, 'min': y, 'today': True}
                    else: dict_[WEEK[z]] = {'max': x, 'min': y}

                with open('weekly.json', 'w') as f:
                    json.dump(dict_,f,indent=1)
                    break
            else:
                with open('weekly.json') as f:
                    reader = json.load(f)
                    print(f'{'-'*14}\n{'Highest-Lowest'}\n{'-'*14}')
                    for g in range(len(WEEK)):

                        i = reader[WEEK[g]]['max']
                        x = reader[WEEK[g]]['min']

                        max_lst.append(i)
                        min_lst.append(x)

                        if 0 < i < 10.0: i = f'0{i}'
                        if 0 < x < 10.0: x = f"0{x}"

                        print(f'{g+1}){i}°C || {x}°C | {WEEK[g]}')


                    print(f'{'-'*24}\n{'Highest-Lowest (average)'}\n{'-'*24}')
                    print(f'{round(sum(max_lst)/len(max_lst), 1)}°C | {round(sum(min_lst)/len(min_lst), 1)}°C')
                    break
                
        except requests.exceptions.RequestException:
            print("Check your connection sir!")
        except(KeyError, ValueError):
            print('City/country not found check the spelling!')


def average():  

        while True:
            try:
                cname = input('Enter the city/country name: ')
                dys = input('Enter the number of searches you wanna see the average of: ').lower()
                days('kregg.csv', int(dys), cname)


                sys.exit()
            except (ValueError,ZeroDivisionError):

                if dys != 'quit':#if the user does not quit nor choose quit or a number this error will be raised
                    print('Invalid input or the given city/country has not been searched this many times!')
                    continue

                else:
                    sys.exit()


def display_saved():#a function to read the csv file without having to go inside of the file 
        with open('kregg.csv') as f:
            for i in f:
                print(i, end='')


command_lst = ['average - to see the average temperature and the windspeed in a certain number of searches',
               'saved - to see the csv file from the terminal',
               'forecast - to see the projected temperature and the windspeed in the upcoming 7 days',
               '<name of country/city> - to see the current temperature of the searched city/country',
               '-h - to list all the functions']


funcs = {
    'average': average,
    'saved': display_saved,
    'forecast': forecast,
    'weekly': set_week,
    '-h': lambda : [print('*',i) for i in command_lst]
}


def main():
    if len(sys.argv) < 2:
        sys.exit("Not enough arguments on the terminal!\n-h for for help")
    command = funcs.get(sys.argv[1])
    if command: command()
    else: get_country()


if __name__ == "__main__":
    main()
    clean()