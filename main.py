import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml

GOOGLE_FORM = "https://forms.gle/t73z3bVCWS9n9Bdp9"
CHROME_DRIVER_PATH = "C:/Users/jamshaid.iqbal/Desktop/Setups/chromedriver.exe"

website = requests.get(
    url="https://www.zameen.com/Rentals/Lahore-1-1.html?price_max=50000", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/102.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,la;q=0.8",
    })

website_html = website.text

soup = BeautifulSoup(website_html, 'html.parser')
links = soup.find_all(name="a", class_="_7ac32433")
links_list = []

for link in links:
    link = f"https://zameen.com{link['href']}"
    links_list.append(link)

prices = soup.find_all(name="div", class_="c4fc20ba")
price_list = []

for price in prices:
    price_list.append(price.getText())


z = 0
for price in price_list:
    if not price.endswith("Thousand"):
        price_list.remove(price)
        # new_list = price.split()
        # new_list[1] = "000"
        # new_price = ','.join(new_list)
        # new_price_list.append(new_price)

for price in price_list:
    if price.endswith("Thousand"):
        new_list = price.split()
        new_list[1] = "000"
        new_price = ','.join(new_list)
        price_list[z] = new_price
        z += 1


places = soup.find_all(name="div", class_="_162e6469")
place_list = []

for place in places:
    place_list.append(place.getText())



chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), chrome_options=chrome_options)

i = 0
for n in range(len(links_list)):
    driver.get(GOOGLE_FORM)

    time.sleep(2)

    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(place_list[i])

    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price_list[i])

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links_list[i])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()
    i += 1
    

print(i)





