import csv
import sys



    
def SaveFile(teacher, level, file_name, lst):

    try:
        average = round(sum(lst)/len(lst), 1)
    except ZeroDivisionError:
        sys.exit('No data entered!')

    dict_ = {
        'teacher': teacher, 'level': level, 'average': average
    }

    fieldnames = ['teacher', 'level', 'average']
    with open(f'{file_name}.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(dict_)
    sys.exit(f'The class average is {average}%')

        
#this constant is for end of years, the reason A1 and A1+ are missing is that they have slightly different way of being calculated
LEVELS = {
    'A2': 0.9,
    'B1': 1/1.14,
    'B1+': 0.84,
    'B2': 0.64
}

def review_test():
    
    teacher = input('Enter the teacher name: ')
    level = input('Enter the level: ')
    lst = []

    while True:

        correct_answers = input('Enter the total correct ans or q for quit: ').lower()
        if correct_answers == 'quit' or correct_answers == 'q':
            SaveFile(teacher, level, 'review', lst)

        else:

            overall = int(correct_answers) / 0.7
            lst.append(overall)
            print(f"{round(overall, 1)}%")

            continue



def a1_end(level, teacher):
    lst = []
    if level == 'A1' or level == 'A1+':

        while True:


            correct_ans = input('Enter the number of correct ans or q for quit: ')
            if correct_ans == 'q': SaveFile(teacher, level, 'end', lst)
            else:

                overall = int(correct_ans) * 70/80
                try:
                    
                    speaking = int(input('Enter the speaking: '))
                    overall += speaking
                    ov = round(overall,1)
                    lst.append(ov)
                    print(f"{ov}%")
                    continue

                except ValueError:

                    print('input an int!') 
                    continue


def handle_levels(level, teacher):

    lst = []
    multiplier = LEVELS.get(level)

    while True:
            
            try:

                reading = input('Enter the reading: ').lower()
                listening = input('Enter the listening: ').lower()

            except ValueError:

                print('Invalid input!')
                continue

            if reading == 'q' or listening == 'q': SaveFile(teacher, level, 'end', lst)

            else:

                try:

                    lr = int(reading) + int(listening)

                except ValueError:
                    print('The last input was not an int!')
                    continue
                pre_total = lr * multiplier

                while True:
                    
                    writing = input('Enter the writing: ')                    
                    speaking = input("Enter the speaking: ")

                    if writing == 'q' or speaking == 'q': SaveFile(teacher, level, 'end', lst)

                    try:

                        total = pre_total + int(writing) + int(speaking)
                        lst.append(total)
                        print(f"{round(total, 1)}%")
                        break

                    except ValueError:

                        print('The last input was not an int!')
                        continue


def end_of_year():
    
    teacher = input("Enter the teacher's name: ")
    level = input('Enter the level: ').capitalize()


    if level in LEVELS: handle_levels(level, teacher)
    elif level in ('A1', 'A1+'): a1_end(level, teacher)
    else: sys.exit('Uknown level!')



def averagebyteacher():
    while True:

        t_type = input('Enter the type of test: ')
        if t_type not in ('end', 'review'):

            print('Only end and review tests are supported!')
            continue

        else:

            how_many_tests = 0

            while True:

                teacher = input('Enter the teacher name: ')
                lst = []
                
                with open(f'{t_type}.csv') as f:
                    reader = csv.DictReader(f)
                    for i in reader:
                        if teacher == i['teacher']:
                            how_many_tests += 1 
                            lst.append(float(i['average']))

                line = '-'*57 #a line over and under data
                try:
                    avrg = sum(lst)/len(lst)
                except ZeroDivisionError:
                    print('The given teacher does not exist in the history!')
                    continue

                print(f'{line}\nThe class average of {teacher} is {round(avrg, 1)}% in the last {how_many_tests} tests\n{line}')
                exit()



commands = ['end (to calculate end of years)',
            'review (calculate review tests)',
            '-h']

dict_ = {
    'end': end_of_year,
    'review': review_test,
    'average': averagebyteacher,
    '-h': lambda : [print("*",i) for i in commands]
}

def main():
    if len(sys.argv) < 2:
        sys.exit('No enough arguments on the terminal!\n' '-h for help')
    command = dict_.get(sys.argv[1].lower())
    if command: command()
    else: sys.exit('Uknown command!' \
          '-h for help')

if __name__ == '__main__':
    main()