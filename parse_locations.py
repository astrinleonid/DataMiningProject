
from greq_open import local_file_open

def parse_locations(soup):
    """
    Returns a list of locations from a job card
    """
    pass


if __name__ == '__main__':

    soup = local_file_open('locations_section.html')
    assert parse_locations(soup) == ['Chicago, IL','Louisville, KY','Huntington, WV']