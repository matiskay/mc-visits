import unicodecsv
import os

from cultura import get_visits_per_day, get_working_days

def get_file_name(date):
    date = date.split('/')
    return date[0] + '-' + date[1] + '-' + date[2]

DIRECTORY_NAME = 'mc-visits'

date = '15/06/2015'

data = get_visits_per_day(date)


if not os.path.isdir(DIRECTORY_NAME):
    os.mkdir(DIRECTORY_NAME)


with open(DIRECTORY_NAME + '/' + get_file_name(date) + '.csv', 'wb') as csvfile:
    writer = unicodecsv.writer(csvfile)

    for d in data:
        writer.writerow(d)
