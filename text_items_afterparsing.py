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
'Occasional travel - Travel required up to 15% of the time.' : (True,15),
'25% or less - Varies' : (True, 25),
'Occasional travel - You may be expected to travel for this position.' : (True,20),
'Occasional travel - You may be expected to travel 1-5 days per month for this position.' : (True, 20),
'Not required' : (False, 0)
}

def parce_salary_text(text):
    """
    Receives the text of the salary field and returns
    a tuple of two integers, representing minimum and maximum salary in dollars
    """
    pass

def parce_dates_text(text):
    """
    Receives the text of the dates field and returns
    a tuple of two strings recognized by SQL as date(in YYYY-MM-DD format)
    """
    pass



def parse_travel_requirements(text):
    """
    Receives the text of the travel_required text field and returns a
    tuple of (boolean, integer) representing general requirement for the travel
    and time percentage (if it can be derived)
    """
    pass




if __name__ == '__main__':

    assert parce_salary_text(SALARY_TEXT) == (56205, 152058)
    assert parce_dates_text(DATES_TEXT) == ('2021-12-01', '2022-11-30')

    for key, value in TRAVEL_REQUIRED:
        assert parse_travel_requirements(key) == value




