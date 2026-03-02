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

    MONTHS = {
        '1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr',
        '5': 'May','6': 'Jun', '7': 'Jul','8': 'Aug',
        '9': 'Sep','10': 'Oct','11': 'Nov','12': 'Dec'
    }

    file_exists = path.isfile('monthly.csv')

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
                final_amount = r['total_money']['amount']

                for i in r:
                    if i == 'total_money': pass
                    else: total += r[i]['amount']

                if final_amount < 0:

                    while True:
                        user = input('Your total amount is negative!\nDo you want to change change it? y/n: ')
                        if user == 'y':
                            new_amount = float(input('Enter the amount you currently have: '))
                            final_amount = 0
                            final_amount += new_amount
                            break
                        elif user == 'n': break
                        else:
                            print('The last input was not y or n!')
                            continue

                else:pass

                r = {
                    'total_money':
                    {
                    'amount': final_amount
                        }
                }

                with open('category.json', 'w') as f:
                    json.dump(r, f, indent=4)

            with open('monthly.csv', 'a', newline='') as f:

                writer = csv.DictWriter(f, fieldnames=['month','amount'])
                if not file_exists:
                    writer.writeheader()
                if date.month == '1': data = Writecsv(MONTHS['12'], total)# if it is January then the in monthly.csv will be written Dec.
                else: data = Writecsv(MONTHS[str(date.month-1)], total)#otherwise just the previous month
                writer.writerow(data.turn_to_dict())
                
        else:
            pass