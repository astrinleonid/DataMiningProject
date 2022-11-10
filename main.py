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

    overview = {}
    # print(soup.find().text)

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

    requirements = []
    requirements_section = soup.find('div', id="requirements")
    reqs = requirements_section.find(class_="usajobs-list-bullets")
    for req in reqs.find_all():
        requirements.append(req.text.strip())
    return {"Requirements": requirements}


def parse_job_cards(url_name):

    soup = html_open(url_name)
    job_notices = soup.find_all(class_="usajobs-search-result--card")
    print(len(job_notices))
    jobs = []
    for job_notice in job_notices:
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
    Top level parser, parses the page with the list of the sections opportunities are grouped to
    """

    titles_section = soup.find("div",class_="usajobs-landing-find-opportunities__section-container")
    titles = soup.find_all("li")
    print(len(titles))
    sections = []
    current_title = ""
    current_index = 0
    for title in titles:
        class_name = title['class'][0]
        if class_name == "usajobs-landing-find-opportunities__section-title":
            current_title = title.text.strip()
            print("Section title =",current_title)
            sections.append({current_title:[]})
            current_index = len(sections)-1
        elif class_name == "usajobs-landing-find-opportunities__job-item":
            print(title.text.strip())
            card_url = ("https://www.usajobs.gov" + title.find("a", href=True)["href"])
            print("Parsing: ",card_url)
            cards = parse_job_cards(card_url)
            sections[current_index][current_title].append({title : cards})
    print(sections['Mathematics'])


if __name__ == "__main__":

    soup = html_open(URL_NAME)
    # soup = BeautifulSoup(file,"html-parser")
    sections = parse_sections(soup)




