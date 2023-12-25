import requests
from bs4 import BeautifulSoup


def scrape_yelp(search_query: str, location: str):
    base_url = 'https://www.restaurants.co.za'
    search_url = f"{base_url}/{search_query.lower()}/{location.lower()}"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    for result in soup.find_all("div", class_="laout_5 direcotry_listing"):
        name = result.find('span', itemprop='name').get_text(strip=True)
        print("Name of the Restaurant: " + name)
        a_content = result.find("a", itemprop="url")
        if a_content:
            link = a_content["href"]
            restaurant_response = requests.get(link)
            restaurant_soup = BeautifulSoup(restaurant_response.text, "html.parser")


            # Extract address and phone number from the restaurant page
            address_element = restaurant_soup.find("li", class_="address")
            phone_number_element = restaurant_soup.find("p", itemprop="telephone")
            email_element = restaurant_soup.find('span', itemprop="email")

            address = address_element.get_text(strip=True) if address_element else "Address not available"
            phone_number = phone_number_element.get_text(
                strip=True) if phone_number_element else "Phone Number not available"
            email = email_element.get_text(strip=True) if email_element else "Email Address not available"
            print("Street Address: " + address)
            print("Phone Number: " + phone_number)
            print("Email Address: " + email)
            print("-------------------")




if __name__ == "__main__":
    search_query = 'gauteng'
    location = ''
    scrape_yelp(search_query, location)
