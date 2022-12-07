
from database_class import text_prepare
from service_setup import config, logger

def parse_overview(soup):
    """
    Parses the overview section of the individual announcement page
    :return: dictionary of the overview items

    """

    overview = {}

    for parameter in soup.find_all(class_=config['tags']["overview_item_class_tag"]):
    # for parameter in soup.find_all(class_="usajobs-joa-summary__item usajobs-joa-summary--beta__item"):
        title_item_soup = parameter.find("h5")
        if title_item_soup == None:
            title_item_soup = parameter.find("h2")
            if title_item_soup == None:
                continue

        title_item = title_item_soup.text
        title_item = title_item.replace('(', ' ')
        title_item = title_item.replace(')', ' ')
        title_item = title_item.replace('&', ' ')
        title_item = title_item.replace('%', ' ')
        title = ("_".join(title_item.strip().split())).lower()
        if title == 'job_family_series':
            overview.update({'job_family_series' : parse_jfs(parameter)})
        elif title == 'locations':
            overview.update({'locations' : parse_locations(parameter)})
        else:
            value = [text_prepare(item.text) for item in parameter.find_all("p")]
            if len(value) > 0:
                overview.update({title: value[0]})
            else:
                overview.update({title: ""})

    return overview

def parse_card_header(soup):
    """
    Parses the overview section of the individual announcement page
    :return: dictionary of the overview items

    """
    card_header = soup.find(class_= config['tags']["card_header_class_teg"])

    title_class = config['tags']["card_title_class_teg"]
    title = card_header.find(class_=title_class).text.strip()
    department_class = config['tags']["dep_name_class_teg"]
    department = card_header.find(class_=department_class).text.strip()
    agency_class = config['tags']["agency_name_class_teg"]
    agency = card_header.find(class_=agency_class).text.strip()

    return {"department" : department, "agency" : agency, "title" : title}

def parse_requirements(soup):
    """
    Parses the Requirements section of of the individual announcement page.
    Returns one-item dictionary with the key "requirements" and the list of requirements as value
    """

    requirements = []
    requirements_section = soup.find('div', id="requirements")
    reqs = requirements_section.find(class_="usajobs-list-bullets")
    for req in reqs.find_all():
        requirements.append(text_prepare(req.text))
    return {"requirements": " ".join(requirements)}

def parse_duties(soup):
    """
    Parses the Requirements section of the individual announcement page.
    Returns one-item dictionary with the key "requirements" and the list of requirements as value
    """

    duties = []
    duties_section = soup.find('div', id="duties")
    duty_list = duties_section.find(class_= config['tags']["bullets_tag"])
    if not duty_list == None:
        for duty in duty_list.find_all():
            duties.append(text_prepare(duty.text))
        return {"duties": " ".join(duties)}
    else:
        return {"duties" : []}
def parse_summary(soup):
    """
        Parses the Summary section of the individual announcement page.
        Returns one-item dictionary with the key "requirements" and the list of requirements as value
    """

    summary_section = soup.find('div', id="summary")
    summary_text_section = summary_section.find('p')
    summary_text = text_prepare(summary_text_section.text)

    return {"summary" : summary_text}

def parse_locations(soup):
    """
    Returns a list of locations from a job card
    """
    locations = []
    for parameter in soup.find_all('li'):
        loc = parameter.find('a')
        if loc != None and 'data-name' in loc.attrs:
            loc_line = [name.strip().strip(',') for name in loc.attrs['data-name'].split()]
            (city, state) = (" ".join(loc_line[:-1]),loc_line[-1])

            locations.append({'city': city, 'state_ID': state})

    return locations

def parse_jfs(soup):
    """
    Returns a list of Job Family (series) from a job card
    """
    jfss = []
    for parameter in soup.find_all('a'):
        if parameter != None :
            jfs_line = [name.strip().strip(',') for name in parameter.text.split()]
            (jfs_name, jfs_number) = (" ".join(jfs_line[1:]),jfs_line[0])
            if jfs_number.isnumeric():
                jfss.append({'name': jfs_name, 'num_index': jfs_number})
            else:
                jfss.append({'name': " ".join(jfs_number, jfs_name), 'num_index': '0'})

    return jfss
