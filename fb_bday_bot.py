import time
import schedule
import requests
import telegram
import csv
import datetime

from config import *


TOKEN = BOT_TOKEN
bot = telegram.Bot(token=TOKEN)

filename = BDAY_CSV_FILE

def get_todays_bdays(filename):
    current_year = datetime.datetime.now().year
    current_date = '{dt.year}-{dt.month}-{dt.day}'.format(dt = datetime.datetime.now())
    bdays = []

    with open(filename) as f:
        headers = f.readline().replace('"', '').replace('\n', '').split(',')

    with open(filename, 'r', encoding="utf8") as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row != headers:
                name, bday = row[0], '-'.join([str(current_year), row[2], row[3]])
                age = str(int(current_year) - int(row[1])) if row[1] != 'null' else 'NA'
                if current_date == bday:
                    bdays.append([name, age])
        
        return bdays

def send_bday_message():
    todays_bdays = get_todays_bdays(filename)
    bday_string = ''
    for name, age in todays_bdays:
        if age == 'NA':
            bday_string += 'Wish {} a Happy Birthday!\n'.format(name)
        else:
            bday_string += '{} is {} today. Wish them a Happy Birthday!\n'.format(name, age)
    bot.sendMessage(chat_id=BOT_CHAT_ID, text=bday_string)

schedule.every().day.at(UPDATE_AT).do(send_bday_message)

while True:
    schedule.run_pending()
    time.sleep(1)
