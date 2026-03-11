import sys
import csv
from datetime import datetime
import collections
import json
import os
from modifier import modify, track_limit

class Checker:
    def checker(self):
        if os.path.getsize('category.json') == 0:
            
            self.currency_ = input('Hello! Before using the app you must specify the currency: ')
            self.total = float(input('Also the total amount of money you have: '))
            with open('category.json', 'w') as f:
                json_dict = {
                    'currency': {
                        'type': str(self.currency_)
                    },
                    "total_money": {
                        'amount': self.total
                    }
                }
                json.dump(json_dict,f,indent=4)
        else:pass
    def currency(self):
        with open('category.json') as f:
            reader = json.load(f)
        return reader['currency']['type']

checker = Checker()
if os.path.getsize('category.json') == 0: pass
else: currency = checker.currency()

date_s = datetime.now().astimezone()


if date_s.month < 10: month = f"0{date_s.month}"
else:month = str(date_s.month)
if date_s.day < 10: day = f"0{date_s.day}"
else:day = str(date_s.day)


local_ = f"{date_s.year}-{month}-{day}"
        

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


def how_much():
    differences = []
    lst = []
    nums = []
    total = 0
    days = int(input("Enter the number of days you wanna see: "))

    with open('date.json') as f:

        reader = json.load(f)
        lines = collections.deque(reader, days)

        for i in lines:
            try:
                day_amount = float((reader[str(i)]['amount']))
                total += day_amount
                nums.append(day_amount)
                lst.append(int(i))
            except KeyError:
                pass
            
        if days > len(nums):
            days = len(nums)
            while True:
                user = input(f'{'-'*52}\nThere are only {days} days available. Still continue? y/n\n{'-'*52}\n> ')
                if user == 'y': break
                elif user == 'n': sys.exit('successfully quit!')
                else: 
                    print('Uknown input!')
                    continue
            
        for index in range(len(lst)):
            try:
                if lst[index+1] - lst[index] > 1:
                    differences.append(lst[index+1]-lst[index])
            except IndexError: pass

        while True:
            if differences:
                for l in range(len(differences)):
                    usr = input(f"{'-'*45}\n{differences[0+l]} day difference found! Still continue? y/n\n{'-'*45}\n> ")
                if usr == 'y':
                    print(f'{'-'*71}\nThe total spent money in {days} days is {total} {currency} | overall a {sum(differences)} day difference')
                    print(f'The average spent money in the {days} days is {round(sum(nums)/len(nums), 1)}{currency}\n{'-'*71}')
                    break
                elif user == 'n': sys.exit('Successfully quit!')
                else:
                    print('Uknown input!')
                    continue
            else:
                print(f'{'-'*48}\nThe total spent money in {days} days is {total} {currency}')
                print(f'The average spent money in the {days} days is {round(sum(nums)/len(nums), 1)}{currency}\n{'-'*48}')
                break
def new():


    def get_data():
        first = input('For: ')
        second = input('Amount: ')
        return first, second
    
    

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

        if str(date_s.day) in reader:
            famount += reader[str(date_s.day)]['amount']

        reader[day] = {
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
    'average': how_much,
    'add': add_to_total,
    'new': new,
    '-h': lambda: [print('*',i) for i in funcs.keys()]
}


def main():
    if len(sys.argv) < 2:
        sys.exit('Not enough arguments on the terminal!\n -h for help`')
    command = funcs.get(" ".join(sys.argv[1:]))# .get() returns boolean or None
    if command: command()
    else: sys.exit('Uknown function!')


if __name__ == "__main__":
    checker.checker()
    track_limit()
    modify()
    main()