import ssl
import time

import requests
import torch
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from selenium import webdriver
import easyocr

user_agent = UserAgent()

chrome_options = Options()

random_user_agent = user_agent.random

print("Случайный User-Agent:", random_user_agent)

chrome_options.add_argument(f"user-agent={random_user_agent}")

url = "https://www.copart.com/lotSearchResults?free=true&query=buick%20encore%20gx"
all_vins = []

site_url = str(input("Enter site link: "))


def get_car(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)
    time.sleep(10)
    with open('data.html', 'w') as file:
        file.write(driver.page_source)
    driver.quit()

    with open('data.html') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    vin = soup.find('span', id="vinDiv").find('span').text.strip()
    clean_vin = str(vin[0:2])
    print(clean_vin)
    imgs = soup.find_all("img", class_="img-responsive")
    reverse_imgs = list(reversed(imgs))
    for img in reverse_imgs:
        try:
            full_url_img = img['full-url']
            response = requests.get(full_url_img)
            with open("img.jpg", "wb") as f:
                f.write(response.content)
            ssl._create_default_https_context = ssl._create_unverified_context
            image_path = 'img.jpg'
            reader = easyocr.Reader(['en'])
            text = reader.readtext(image_path)
            if len(text) != 0:
                for i in text:
                    if clean_vin in i[1]:
                        all_vins.append(i[1])
                        print(i[1])
                        return i[1]
        except :
            pass


def get_cars_url(url):
    cars_url = []
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)
    time.sleep(5)
    with open('data.html', 'w') as file:
        file.write(driver.page_source)
    driver.quit()

    with open('data.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cars_a = soup.find_all("a", class_="ng-star-inserted")
    for a in cars_a:
        try:
            if not f"https://www.copart.com{a['href']}" in cars_url:
                cars_url.append(f"https://www.copart.com{a['href']}")
        except:
            pass
    return cars_url


def main(site_url):
    all_cars_urls = get_cars_url(site_url)
    print(all_cars_urls)

    count = 1
    for url in all_cars_urls:
        print(count)
        print(url)
        try:
            get_car(url)
        except:
            pass
        count += 1
    print(all_vins)

main(site_url)
# https://www.copart.com/lotSearchResults?free=true&query=buick%20encore
# ['KL4CJASB8JB662777', 'KL4CJGSMSKB732998', 'KLACJESB5KB959420', 'KL4CJASB7KB8B4O5T', 'KLACJASBAHB188126', 'KLACJFSBSEBGRA7074', 'KLACJASB9KB761450', 'KL4CuCSB9GB633390', 'KLACJFSBXFB133335', 'KL4CJASb3HBOOC67E', 'KL4CJCSB8GB705485 ', 'KL4CJGSBGEB556305', 'KLAMMDSLBLB126176']