from bs4 import BeautifulSoup

page = open("Sections.html","r")
soup = BeautifulSoup(page, "html.parser")


def parse_sections(soup):
    titles_section = soup.find("div",class_="usajobs-landing-find-opportunities__section-container")
    titles = soup.find_all("li")
    print(len(titles))
    sections = []
    for title in titles:
        class_name = title['class'][0]
        if class_name == "usajobs-landing-find-opportunities__section-title":
            current_title = title.text.strip()
            sections.append({current_title:[]})
        else:
            print(title.text.strip())
            card_url = title.find("a", href=True)["href"]
            cards = parse_job_cards(url_name)
            print(card_url)
            sections[current_title].append({title : cards})
    print(sections['Mathematics'])



    #     details_url = job_notice.find("a", href=True)["href"]
    #     details = html_open(details_url)
    #     job_card = parse_overview(details)
    #     job_card.update(parse_requirements(details))
    #     title = job_notice.find(class_ ="usajobs-search-result__title").text.strip()
    #     department = job_notice.find(class_="usajobs-search-result__department").text.strip()
    #     job_card.update({"Title" : title})
    #     job_card.update({"Department" : department})
    #     jobs.append(job_card )
    #
    #
    # return jobs
parse_sections(soup)