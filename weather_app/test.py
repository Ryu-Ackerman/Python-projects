days = {
    '1': 'th',
    '2': 'nd',
    '3': 'rd'
}

lst = ['1','2','3','4','5','6']
sting = 'th'


days = {
    '1': 'st',
    '2': 'nd',
    '3': 'rd'
}


for i in range(4,32):
    days[f'{i}'] = 'th'


for x,y in zip(lst,days):
    print(f'{x} {days[x]}')