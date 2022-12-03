
from greq_open import local_file_open

def parse_locations(soup):
    """
    Returns a list of locations from a job card
    """
    locations = []
    for parameter in soup.find_all('li'):
        loc = parameter.find('a')
        if 'data-name' in loc.attrs:
            # [city, state] = ['Mobile', 'AL']
            # print(   [name.strip().strip(',') for name in loc.attrs['data-name'].split()])
            loc_line = [name.strip().strip(',') for name in loc.attrs['data-name'].split()]
            (city, state) = (" ".join(loc_line[:-1]),loc_line[-1])
            # locations.append({'city' : city, 'state_ID' : state, 'lat' : float(loc.attrs['data-coord-lat']), 'long' : float(loc.attrs['data-coord-long'])})
            locations.append({'city': city, 'state_ID': state})

            # print( loc.attrs['data-name'])
            # print(loc.attrs['data-coord-lat'])
            # print(loc.attrs['data-coord-long'])
    print(len(locations))
    return locations



if __name__ == '__main__':

    soup = local_file_open('locations_section.html')
    result = parse_locations(soup)
    # print(result)
    assert result[0] == {'city' : 'Mobile', 'state_ID' : 'AL', 'lat' : '30.6864', 'long' : '-88.0532'}