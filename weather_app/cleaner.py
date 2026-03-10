import csv
from timezonefinder import TimezoneFinder
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import requests


WEEK = [
    'Monday','Tuesday','Wednesday',
    'Thursday','Friday','Saturday',
    'Sunday'
]



def clean():
    columns = ['city', 'temperature', 'windspeed', 'date-time']
    lines = []

    with open('kregg.csv') as f:

        reader = csv.DictReader(f)
        for i in reader:
            lines.append(i)

        if len(lines) > 30:#if the number of searches exceed 30 delete one from the top of csv file
            lines.pop(0)#remove the first item

    with open('kregg.csv', 'w', newline='') as f:#writing over the csv after storing everything to a list and modifying it
        
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for i in lines:
            writer.writerow(i)

def checker():
    with open('weekly.json') as f:
        reader = json.load(f)
        tf = TimezoneFinder()
        zone = tf.timezone_at(
            lng=reader['configs']['longitude'],
            lat=reader['configs']['latitude']
        )

        current = datetime.now(ZoneInfo(zone))
    
        
        try:
            starting_date = reader['configs']['starting_date'][9]
            if int(starting_date) + 7 != current.day:
                api3 = f"https://api.open-meteo.com/v1/forecast?latitude={reader['configs']['latitude']}&longitude={reader['configs']['longitude']}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&past_days=7&timezone=auto"
                r = requests.get(api3)
                j = r.json()
                day = current.strftime('%A')#finding the day of the week with a given city/country name

                inde = [inde for inde,h in enumerate(WEEK) if h == day][0]
                maxt = j['daily']['temperature_2m_max']
                mint = j['daily']['temperature_2m_min']

                y = len(WEEK[0:inde])
                starting_date = j['daily']['time'][6]

                dict_ = {"configs":{
                            "country": reader['configs']['country'],
                            'longitude': reader['configs']['longitude'],
                            'latitude': reader['configs']['latitude'],
                            'starting_date': starting_date}}

                for x,y,z, in zip(maxt[7-y:7+(7-y)], mint[7-y:7+(7-y)], range(len(WEEK))):

                    if WEEK[z] == day: dict_[WEEK[z]] = {'max': x, 'min': y, 'today': True}
                    else: dict_[WEEK[z]] = {'max': x, 'min': y}

                with open('weekly.json', 'w') as f:
                    json.dump(dict_,f,indent=1)
            else:
                pass
        except KeyError:
            pass

