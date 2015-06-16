import unicodecsv
import os

from cultura import get_visits_per_day, get_working_days

def get_file_name(date):
    date = date.split('/')
    return date[0] + '-' + date[1] + '-' + date[2]


def write_to_csv(date):
    with open(DIRECTORY_NAME + '/' + get_file_name(date) + '.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile)

        for d in data:
            writer.writerow(d)

DIRECTORY_NAME = 'mc-visits'


if not os.path.isdir(DIRECTORY_NAME):
    os.mkdir(DIRECTORY_NAME)


working_days = get_working_days((2013, 1, 1), (2015, 6, 15))

for date in working_days:
    data = get_visits_per_day(date)
    print 'Getting data from %s' % date

    if len(data) > 0:
        write_to_csv(date)
    else:
        print '---> No data for %s' % date
