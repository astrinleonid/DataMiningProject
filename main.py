import requests
from bs4 import BeautifulSoup

url_name = 'https://www.usajobs.gov/Search/ExploreOpportunities?Series=1550'

def html_open(url_name):

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


def parse_job_cards(soup):

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

if __name__ == "__main__":

    soup = html_open(url_name)
    jobs = parse_job_cards(soup)
    for job in jobs:
        print(job["Department"])
        print(job("Salary"))
        print(job["Open&Closing dates"])