
# Python projects

Each project above has been made because common apps lack something that these projects have filled and solved a problem that I and, most probably, others have struggled with.

# Downloaded_stuff
This project uses yt_dlp and downloads videos and songs. I could've used already made websites or bots that are way faster than this but this projects automatically configures everything and even sets the location of where the downloaded item should be sent which is most of the time painful while using external downloaders.

# Expenses
Expenses folder inside, admittedly, has a lot of files but they all have a purpose. Firstly there is the main file expense_tracker.py that handles all the main tasks, such as adding the new expense, file i/o, average calculator from .json files. Additionally, there is modifier.py that takes care of automating the month tracking and sets the previous month to the current month in the date.json file and writes the total expenditure to the monthly.csv which requires nothing more than the usage of the app.

# Polyglot calculator
Before we continue I want to gently tell the reader that I work at the Polyglot language school as an academic support and the main duties include helping the teacher we are attached to, helping students with their tasks and homework, conducting extra lessons and lastly and the most dreadful part checking tests. Checking tests require first of all counting all the correct answers of students and depending on the level of the group's English level and the test type - review or end of year - calculating the overall is pretty frustrating. Thus, I made this to easily calculate everything and save them safely to .csv files with the teacher's name and the group level. The app works by the user typing in the teacher's name, the level the type of test. Afterwards, the user inputs the total number of correct answers on the test of a single student while the app responds with the percentage that the student scored in the test. Finally, when the user types in all the students and presses "q" to quit the app gives the class average of the teacher and the group and saves it to the csv file. The app works in an infinite loop, unless the user types "q", the app will run continuously. 

# Weather app
This looks like a casual weather app and it is, it gets the current weather temperature and the windspeed with the user typing in the city/country name, gives you a full 7 day forecast with dates, days of the week, temperature and the windspeed and the average expected temperature and windspeed in the upcoming 7 days. The app includes average calulator as well. There is the kregg.csv that saves all the info about the city/country when searched. When the user wants to see the average temperature in the last certain number of searches this app hands them the data. The csv file does not store more than 31 searches because otherwise it would become too heavy and that is handled by the cleaner.py that keeps track of it.
