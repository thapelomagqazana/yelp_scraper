import logging
import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(filename="scraper.log", level=logging.INFO)


def get_search_url(search_query: str, location: str) -> str:
    base_url = 'https://www.restaurants.co.za'
    return f"{base_url}/{search_query.lower()}/{location.lower()}"


def scrape_yelp(search_url: str):
    try:
        ua = UserAgent()
        headers = {"User-Agent": ua.random}

        req = urllib.request.Request(search_url, headers=headers)
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser")

        for result in soup.find_all("div", class_="laout_5 direcotry_listing"):
            name = result.find('span', itemprop='name').get_text(strip=True)
            logging.info("Name of the Restaurant: " + name)
            a_content = result.find("a", itemprop="url")
            if a_content:
                link = a_content["href"]
                restaurant_req = urllib.request.Request(link, headers=headers)
                restaurant_html = urllib.request.urlopen(restaurant_req).read()
                restaurant_soup = BeautifulSoup(restaurant_html, "html.parser")

                # Extract address and phone number from the restaurant page
                address_element = restaurant_soup.find("li", class_="address")
                phone_number_element = restaurant_soup.find("p", itemprop="telephone")
                email_element = restaurant_soup.find('span', itemprop="email")

                address = address_element.get_text(strip=True) if address_element else "Address not available"
                phone_number = phone_number_element.get_text(
                    strip=True) if phone_number_element else "Phone Number not available"
                email = email_element.get_text(strip=True) if email_element else "Email Address not available"
                logging.info("Street Address: " + address)
                logging.info("Phone Number: " + phone_number)
                logging.info("Email Address: " + email)
                logging.info("-------------------")

    except urllib.error.HTTPError as e:
        logging.error(f"HTTPError while scraping {search_url}: {e}")
    except urllib.error.URLError as e:
        logging.error(f"URLError while scraping {search_url}: {e}")
    except Exception as e:
        logging.error(f"Error scraping {search_url}: {e}")


if __name__ == "__main__":
    search_query = 'gauteng'
    location = ''
    search_url = get_search_url(search_query, location)
    scrape_yelp(search_url)
