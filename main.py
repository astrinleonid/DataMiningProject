import requests
from bs4 import BeautifulSoup

URL_NAME = 'https://www.usajobs.gov/?c=opportunities'
OVERVIEW_ITEMS = ('pay_scale_&_grade',
                'telework_eligible',
                'travel_required',
                'relocation_expenses_reimbursed',
                'appointment_type',
                'work_schedule',
                'service',
                'promotion_potential',
                'job_family_(series)',
                'supervisory_status',
                'security_clearance',
                'drug_test',
                'position_sensitivity_and_risk',
                'trust_determination_process')


class Value_Counter:

    def __init__(self, key_list):
        self.__item_counter__ = {}
        for key in key_list:
            self.__item_counter__.update({key : []})

    def add_card(self, card):
        for key, value in card.items():
            if key in OVERVIEW_ITEMS:
                if value not in self.__item_counter__[key]:
                    self.__item_counter__[key].append(value)

    def store_values(self,filename, no_records):

        with open(filename, 'a') as file:
            file.write("\n\n\nTotally " + str(no_records) + "records analysed\n")
            for key, value in self.__item_counter__.items():
                file.write("\n" + key + "  Take " + str(len(value)) + " values :  " + str(value))







def html_open(url_name):
    """
    Opens web page at url_name
    Returns the soup of the whole page
    """
    page = requests.get(url_name)
    return BeautifulSoup(page.content, "html.parser")


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

    return {"Department" : department, "Agency" : agency, "Title" : title}

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
    return {"Requirements": requirements}

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
            duties.append((duty.text.strip(),hash(duty.text.strip())))
        return {"Duties": duties}
    else:
        return {"Duties" : []}
def parse_summary(soup):

    summary_section = soup.find('div', id="summary")
    summary_text_section = summary_section.find('p')
    summary_text = summary_text_section.text.strip()

    return {"Summary" : summary_text}


def parse_job_card(details):

    job_card = {**parse_card_header(details), **parse_overview(details), **parse_summary(details)}
    job_card.update(parse_requirements(details))
    job_card.update(parse_duties(details))
    return job_card

def parse_job_cards(url_name,limit=-1):
    """
    Parses the page with list of the cards.
    Returns list of dictionaries (each card is represented by a dictionary)
    """
    v_counter = Value_Counter(OVERVIEW_ITEMS)
    soup = html_open(url_name)
    count = int(soup.find(class_="usajobs-search-controls__results-count").text.split()[0].strip())
    print("Cards on page: ",count)
    page_number = 1
    jobs = []
    hashes = []
    duties_number = 0
    while True:
        print("Page number = ",page_number)
        url_name_wpage = url_name + "&sort=enddate&page=" + str(page_number)
        print("scraping from url ", url_name_wpage)
        soup = html_open(url_name_wpage)
        job_notices = soup.find_all(class_="usajobs-search-result--card")
        number_of_cards = len(job_notices)
        print("Cards on this page: ",number_of_cards)
        page_number += 1
        for i, job_notice in enumerate(job_notices):
            if i == limit: #limiting output for debugging
                break

            details_url = job_notice.find("a", href=True)["href"]
            details = html_open(details_url)
            job_card = parse_job_card(details)

            v_counter.add_card(job_card)
            jobs.append(job_card )
            for duty, duty_hash in job_card["Duties"]:
                duties_number += 1
                if duty_hash not in hashes:
                    hashes.append(duty_hash)

        if number_of_cards < 25:
            break
    print(f"Total different duties found: {duties_number} from them unique {len(hashes)} ")
    v_counter.store_values("values.txt",count)
    return jobs

def parse_sections(soup):

    """
    Top level parser, parses the page with the list of the sections opportunities are grouped to topics.
    Return the list of the dictionaries: Name of the section as key, dictionary of embedded sections as value.
    Each embedded dictionary contains subsection names as keys, list of cards as value
    """
    titles_section = soup.find("div",class_="usajobs-landing-find-opportunities__section-container")
    class_of_title = "usajobs-landing-find-opportunities__section-title"
    class_of_item = "usajobs-landing-find-opportunities__job-item"
    titles = soup.find_all("li",class_=[class_of_item,class_of_title])
    sections = []
    current_title = ""
    current_index = 0
    out_file = ""
    for title in titles:

        class_name = title['class'][0]

        if class_name == class_of_title:
            current_title = title.text.strip()
            print("Section title =",current_title)
            sections.append({current_title:[]})
            out_file += "\n\n" + current_title + "\n"
            current_index = len(sections)-1
        elif class_name == class_of_item:
            title_string = title.text.strip()
            print(title_string)
            card_url = ("https://www.usajobs.gov" + title.find("a", href=True)["href"])
            print("Parsing: ",card_url)
            cards = parse_job_cards(card_url)
            sections[current_index][current_title].append({title.text.strip() : cards})



if __name__ == "__main__":

    soup = html_open(URL_NAME)
    # soup = BeautifulSoup(file,"html-parser")
    sections = parse_sections(soup)




