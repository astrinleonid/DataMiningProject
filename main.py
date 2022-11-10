import requests
from bs4 import BeautifulSoup

URL_NAME = 'https://www.usajobs.gov/?c=opportunities'



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
            title = title_item.text.strip()
            value = [item.text.strip() for item in parameter.find_all("p")]

        # if title == "Open & closing dates":
        #     if len(value) > 0:
        #         dates_in_string = value[0].split()
        #     if len(dates_in_string) < 7:
        #         print(value)
        #     else:
        #         overview.update({"Opening date":dates_in_string[4],"Closing date":dates_in_string[6]})
        # elif title == "Salary": m
        #     overview.update({"Lower range": value[0].split()[0], "Upper range": value[0].split()[2]})
        # else :
            overview.update({title: value[0]})
    return overview

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


def parse_job_cards(url_name,limit=-1):
    """
    Parses the page with list of the cards.
    Returns list of dictionaries (each card is represented by a dictionary)
    """

    soup = html_open(url_name)
    job_notices = soup.find_all(class_="usajobs-search-result--card")
    print(len(job_notices))
    jobs = []
    for i, job_notice in enumerate(job_notices):
        if i == limit: #limiting output for debugging
            break
        details_url = job_notice.find("a", href=True)["href"]
        details = html_open(details_url)
        job_card = parse_overview(details)
        job_card.update(parse_requirements(details))
        title = job_notice.find(class_ ="usajobs-search-result__title").text.strip()
        department = job_notice.find(class_="usajobs-search-result__department").text.strip()
        job_card.update({"Title" : title})
        job_card.update({"Department" : department})
        jobs.append(job_card )

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
    print(len(titles))
    sections = []
    current_title = ""
    current_index = 0
    out_file = ""
    for title in titles:

        class_name = title['class'][0]

        if class_name == class_of_title:
            print("Header found: ",class_name)
            if len(sections) > 0:
                print(sections[current_index])
            current_title = title.text.strip()
            print("Section title =",current_title)
            sections.append({current_title:[]})
            out_file += "\n\n" + current_title + "\n"
            current_index = len(sections)-1
        elif class_name == class_of_item:
            print(title.text.strip())
            card_url = ("https://www.usajobs.gov" + title.find("a", href=True)["href"])
            print("Parsing: ",card_url)
            cards = parse_job_cards(card_url)
            print("Cards in section", cards)
            out_file += str(cards) + "\n\n"
            sections[current_index][current_title].append({title.text.strip() : cards})
            file = open("output.txt","w")
            file.write(out_file)
            file.close


if __name__ == "__main__":

    soup = html_open(URL_NAME)
    # soup = BeautifulSoup(file,"html-parser")
    sections = parse_sections(soup)




