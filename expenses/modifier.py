import json
from datetime import datetime
import csv
from os import path

class Writecsv():

    def __init__(self, month, amount):
        self.month = month
        self.amount = amount

    def turn_to_dict(self):
        dict_ = {
            'month': self.month,
            'amount': self.amount
        }
        return dict_
        

def modify():
    date = datetime.now().astimezone()


    MONTHS = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr',
            '5': 'May','6': 'Jun', '7': 'Jul','8': 'Aug',
            '9': 'Sep','10': 'Oct','11': 'Nov','12': 'Dec'
    }

    file_exist = path.isfile('monthly.csv')

    with open('date.json') as f:
        total = 0
        reader = json.load(f)
        if str(date.month) not in reader:
            reader = {
                f'{date.month}': 
                {
                    'month': MONTHS[f'{date.month}']
                }
            }
            with open('date.json', 'w') as file:
                json.dump(reader, file ,indent=4)
            with open('category.json') as f:
                r = json.load(f)
                for i in r:
                    if i == 'total_money':
                        pass
                    else:
                        total += r[i]['amount']
                r = {
                    'total_money':
                    {
                    'amount': r['total_money']['amount']
                        }
                }
                with open('category.json', 'w') as f:
                    json.dump(r, f, indent=4)
            with open('monthly.csv', 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['month','amount'])
                if not file_exist:
                    writer.writeheader()
                data = Writecsv(MONTHS[str(date.month)], total)
                writer.writerow(data.turn_to_dict())
        else:
            pass