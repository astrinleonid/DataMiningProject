from bs4 import BeautifulSoup
import re


def parse_overview(soup):
    """
    Parses the overview section of the individual announcement page
    :return: dictionary of the overview items

    """

    overview = {}

    for parameter in soup.find_all(class_="usajobs-joa-summary__item usajobs-joa-summary--beta__item"):
        title_item = parameter.find("h5")
        if title_item != None:
            title = ("_".join(title_item.text.strip().split())).lower()
            value = [item.text.strip() for item in parameter.find_all("p")]
            overview.update({title: value[0]})
    return overview

def parse_card_header(soup):
    """
    Parses the overview section of the individual announcement page
    :return: dictionary of the overview items

    """
    card_header = soup.find(class_="usajobs-joa-banner__body usajobs-joa-banner--pilot__body")

    title_class = "usajobs-joa-banner__title"
    title = card_header.find(class_=title_class).text.strip()
    department_class = "usajobs-joa-banner__dept"
    department = card_header.find(class_=department_class).text.strip()
    agency_class = "usajobs-joa-banner__agency usajobs-joa-banner--v1-3__agency"
    agency = card_header.find(class_=agency_class).text.strip()
    # TODO: store in the database
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
        requirements.append(req.text.strip())
    return {"requirements": " ".join(requirements)}

def parse_duties(soup):
    """
    Parses the Requirements section of of the individual announcement page.
    Returns one-item dictionary with the key "requirements" and the list of requirements as value
    """

    duties = []
    duties_section = soup.find('div', id="duties")
    duty_list = duties_section.find(class_="usajobs-list-bullets")
    if not duty_list == None:
        for duty in duty_list.find_all():
            duties.append(duty.text.strip())
        return {"duties": " ".join(duties)}
    else:
        return {"duties" : []}
def parse_summary(soup):

    summary_section = soup.find('div', id="summary")
    summary_text_section = summary_section.find('p')
    summary_text = summary_text_section.text.strip()

    return {"summary" : summary_text}
