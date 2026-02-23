import sys
import csv
from datetime import datetime
import collections
import json     

class Local:

    def __init__(self, year, month, day):

        self.year = year
        self.month = month
        self.day = day


date_s = datetime.now().astimezone()
local = Local(date_s.year, date_s.month, date_s.day)


if local.month < 10: local.month = f"0{local.month}"
if local.day < 10: local.day = f"0{local.day}"
local_ = f"{local.year}-{local.month}-{local.day}"
        

class Transaction:
        
        def __init__(self, category, amount, date_s):
            self.category = category
            try:
                self.amount = float(amount)
            except ValueError as e:
                raise e('The amount needs to be an int or float')
            self.date_s = date_s

        def turn_dict(self):
            return {
                "category": self.category,
                "amount": self.amount,
                "date": self.date_s
            }
        

def get_data():
    first = input('For: ')
    second = input('Amount: ')
    return first, second


def how_much():
    total = 0
    days = int(input("Enter the number of days you wanna see: "))
    lst = []
    nums = []
    with open('test_date.json') as f:

        reader = json.load(f)
        lines = collections.deque(reader, days)
        for i in lines:
            if days > len(lines): sys.exit('there arent as many days in the history')
            else:
                day_amount = float((reader[str(i)]['amount']))
                total += day_amount
                nums.append(day_amount)
                lst.append(int(i))
            
    print(f'The total spent money on the given days is {total}')
    print(f'The average spent money on the given days is {sum(nums)/len(nums)}')


def new():

    while True:

        with open("tracker.csv", 'a', newline="") as f:

            fieldnames = ['category', 'amount','date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            category, amount= get_data()
            t = Transaction(category, amount, local_)
            writer.writerow(t.turn_dict())
            
        with open('category.json') as f:

            fjson = json.load(f)
            if category in fjson:

                namount = fjson[category]['amount'] + float(amount)

            else:

                namount = float(amount)

            fjson['total_money']['amount'] -= float(amount)
            fjson[category] = {
                'amount': namount
                }
            
            with open('category.json', 'w') as f:
                json.dump(fjson, f, indent=4)

        with open('date.json') as f:
                reader = json.load(f)

        famount = float(amount)

        if str(local.day) in reader:
            famount += reader[str(local.day)]['amount']

        reader[str(local.day)] = {
            'amount': famount
            }
        
        with open('date.json', 'w') as f:
            json.dump(reader, f, indent=4)
            break

        
def add_to_total():

    with open("category.json") as f:

        dict_ = json.load(f)
        user = float(input('Enter the amount you wanna add: '))
        dict_['total_money']['amount'] += user
        
    with open('category.json', "w") as f:
        json.dump(dict_,f, indent=4)


funcs = {
    'last': how_much,
    'add': add_to_total,
    'new': new,
    '-h': lambda: [print('*',i) for i in funcs.keys()]
}


def main():
    if len(sys.argv) < 2:
        sys.exit('Not enough arguments on the terminal!\n -h for help`')
    command = funcs.get(" ".join(sys.argv[1:]))# .get() returns boolean or None
    if command:
        command()
    else:
        sys.exit('Uknown function!')


if __name__ == "__main__":
    main()