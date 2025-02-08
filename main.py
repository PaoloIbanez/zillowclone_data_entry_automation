from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup





url = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(url)
web_html = response.text
soup = BeautifulSoup(web_html, "html.parser")

all_listings = soup.select('.StyledPropertyCardDataWrapper')
print(f"Found {len(all_listings)} listings")
addresses = []
prices = []
links = []

for listing in all_listings:
    price_tag = listing.select_one('span[data-test="property-card-price"]')
    price_text = price_tag.get_text() if price_tag else ""
    price_clean = price_text.split("+")[0].strip()

    address_tag = listing.select_one('address[data-test="property-card-addr"]')
    address_text = address_tag.get_text() if address_tag else ""
    address_clean = address_text.replace("\n", "").strip()

    link_tag = listing.select_one('a[data-test="property-card-link"]')
    link_href = link_tag["href"] if link_tag else ""
    # If link is relative, prepend the main domain if needed
    if "http" not in link_href:
        link_href = "https://appbrewery.github.io" + link_href
    print("Price:", price_clean, " Address:", address_clean, " Link:", link_href)


    prices.append(price_clean)
    addresses.append(address_clean)
    links.append(link_href)


# now to the form
driver = webdriver.Chrome()
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeXIaZ_g8eNCHmGNcbmpFsLX0GF_k_4j85lgrM8_Goh54Ea5Q/viewform?usp=header"  # from step 1

for i in range(len(prices)):
    # 1. Go to the form
    driver.get(form_url)
    time.sleep(2)

    # 2. Fill price
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(prices[i])

    # 3. Fill address
    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(addresses[i])

    # 4. Fill link
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(links[i])

    # 5. Click Submit
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    time.sleep(1)

