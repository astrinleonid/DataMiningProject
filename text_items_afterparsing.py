import re
import numpy as np
import pandas as pd


SALARY_TEXT = """
    $56,205 - $152,058 per year\r\n                                            Salary is determined by duty location and grade of the position being filled.
"""
DATES_TEXT = """
12/01/2021 to 11/30/2022
"""

JOB_FAMILY_SERIES = """
0801 General Engineering
"""
TRAVEL_REQUIRED = {
'Occasional travel - Travel required up to 15% of the time.' : (1,15),
'25% or less - Varies' : (1, 25),
'Occasional travel - You may be expected to travel for this position.' : (1,20),
'Occasional travel - You may be expected to travel 1-5 days per month for this position.' : (1, 20),
'Occasional travel - Travel will be required three or more times per year and up to three consecutive weeks.' : (1, 20),
'Not required' : (0, 0)
}

def parce_salary_text(text):
    """
    Receives the text of the salary field and returns
    a tuple of two integers, representing minimum and maximum salary in dollars
    """
    range_from = float(re.sub("[$,]", "", (text.split('per year')[0].split()[0])))
    range_to = float(re.sub("[$,]", "", (text.split('per year')[0].split()[2])))

    # range_from, range_to = re.sub("[^$0-9]", "", text).split('$')[1::]
    return range_from, range_to

def parce_dates_text(d):
    """
    Receives the text of the dates field and returns
    a tuple of two strings recognized by SQL as date(in YYYY-MM-DD format)
    """
    from_date = d.split()[0]
    from_date = pd.to_datetime(from_date, format="%m/%d/%Y").date().strftime('%Y/%m/%d')
    to_date = d.split()[2]
    to_date = pd.to_datetime(to_date, format="%m/%d/%Y").date().strftime('%Y/%m/%d')
    return from_date.replace('/', '-'), to_date.replace('/', '-')


def parse_travel_requirements(text):
    """
    Receives the text of the travel_required text field and returns a
    tuple of (boolean, integer) representing general requirement for the travel
    and time percentage (if it can be derived)
    """

    pattern = '[0-9]{1,2}%'
    percents = re.findall(pattern, text)
    if len(percents) > 0:
        return (1, int(percents[0].strip('%')))
    elif text.lower().find('occasional') >= 0:
        return (1, 20)
    else:
        return (0, 0)


if __name__ == '__main__':
    print(parce_salary_text(SALARY_TEXT))
    # assert parce_salary_text(SALARY_TEXT) == (56205, 152058)
    # assert parce_dates_text(DATES_TEXT) == ('2021-12-01', '2022-11-30')
    #
    for key, value in TRAVEL_REQUIRED.items():
        print(parse_travel_requirements(key))
        assert parse_travel_requirements(key) == value




