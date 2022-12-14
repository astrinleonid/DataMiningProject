from greq_open import *

URL_NAME = "https://www.usajobs.gov/job/683987500"


if __name__ == "__main__":

    try:
        single_url_open(URL_NAME)
    except FileNotFoundError as er:
        print(f"File open unsucsessfull, {er}")