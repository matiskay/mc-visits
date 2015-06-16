import requests
import json
import urllib

from bs4 import BeautifulSoup
from w3lib.html import remove_tags
from tabulate import tabulate

import calendar
import pprint

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]

def get_value(record):
    return unicode(' '.join(remove_tags(unicode(record)).split()))

#lstVisitasResult_page 5

def make_request(date, page=None):
    payload = {
        'VisitaConsultaQueryForm[feConsulta]': date,
        'yt0': 'Consultar',
    }

    params = {
        'r': 'consultas/visitaConsulta/index',
    }

    if page:
        params['lstVisitasResult_page'] = page
        params['r'] = 'consultas/visitaConsulta/updateVisitasConsultaResultGrid'
        params['ajax'] = 'lst-visitas-consulta-result-grid'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # TODO: Check if there is an error or not
    r = requests.post('http://visitas.mcultura.gob.pe/index.php', params=params, data=urllib.urlencode(payload), headers=headers)
    return r.text


def parser(html_doc, skip_header=False):
    response = BeautifulSoup(html_doc)

    table = response.find('table', class_='items')
    rows = table.findAll('tr')

    data = []

    for index, row in enumerate(rows):
        if index == 0 and skip_header:
            continue

        d = []
        for cel in row:
            d.append(get_value(cel))

        data.append(d)

    pagination = response.find('ul', class_='yiiPager').findAll('li', class_='page')
    number_of_pages = len(pagination)

    return data, number_of_pages

# Get the working days from a start time to and end_date
# working day: Monday to Friday. We are not considering holydays

# TODO: Add day range
def get_working_days(initial, final):
    calendar.setfirstweekday(calendar.SUNDAY)
    initial_year = initial[0]
    initial_month = initial[1]
    initial_day = initial[2]

    final_year = final[0]
    final_month = final[1]
    final_day = final[2]

    # Only one year
    if final_year == initial_year:
        for month in range(initial_month, final_month + 1):
            if month == initial_month:
                print_days(final_year, month, initial_day, 31)
            elif month == final_month:
                print_days(final_year, month, 0, final_day)
            else:
                print_days(final_year, month, 0, 31)

    # Handle More than one year
    else:
        years = range(initial_year, final_year + 1)

        number_of_years = len(years)
        index = 1

        for year in years:
            if index == 1:
                for month in range(initial_month, 13):
                    if month == initial_month:
                        print_days(year, month, initial_day, 31)
                    else:
                        print_days(year, month, 0, 31)

            elif index == number_of_years:
                for month in range(1, final_month + 1):
                    if month == final_month:
                        print_days(year, month, 0, final_day)
                    else:
                        print_days(year, month, 0, 31)
            else:
                for month in range(1, 13):
                    print_days(year, month)

            index = index + 1

def print_days(year, month, initial_day, final_day):
    for week in calendar.monthcalendar(year, month):
        for day in WEEKDAYS:
            if week[day] and (week[day] >= initial_day and week[day] <= final_day):
                print '{:02d}/{:02d}/{}'.format(week[day], month, year)



if __name__ == '__main__':
    # y /m /d
    #print get_working_days((2014, 5, 1), (2015, 2, 1))
    #get_working_days((2014, 5, 25), (2015, 6, 24))

    #html_doc = make_request('18/02/2015')
    #data, number_of_pages = parser(html_doc)

    #print tabulate(data)
    #print number_of_pages
