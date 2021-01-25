# ----------------------- Imported Libraries -----------------------
# imports for web scraper
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import csv
import re

# imports for data analysis
import pandas as pd


# ----------------------- Methods -----------------------

# Scrape each page of the target site
def scrape_pages(base_url):
    # Use Selenium and Chrome driver to fetch page
    # This helps get around issues with javascript and loading time
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option('prefs', {
        'geolocation': True
    })
    driver = webdriver.Chrome('chromedriver', options=options)

    # We will loop through each page of results
    # A 404 will break the loop
    page = 1
    while True:
        print(f'>>> Scraping page {page}')

        # Page-specific URLs
        url = f'{base_url}?page={page}'

        # Check status code
        # When page is larger than the max, we get a 404
        response = requests.get(url)
        if response.status_code != 200:
            break

        # Wait 5 seconds for page to fully load
        # Then fetch html
        driver.get(url)
        time.sleep(5)
        source=driver.page_source

        # Parse html with BeautifulSoup using recommended lxml parser
        soup = BeautifulSoup(source, 'lxml')
        container = soup.find('div', class_='view shop catalog')
        results = container.find('ol', class_='cell-container')
        listings = results.find_all('li', class_='cell-wrapper')

        for listing in listings:
            save_listing(listing)

        page = page + 1 # increment page

# Save data from each listing to a CSV file
def save_listing(listing):
    # Find title if applicable
    title = listing.find('div', class_='cell-title-text').get_text().strip() \
        if listing.find('div', class_='cell-title-text') else None

    # Find size if applicable
    size = listing.find('div', class_='cell-product-size').get_text().strip() \
        if listing.find('div', class_='cell-product-size') else None

    # Find aisle if applicable
    aisle = listing.find('div', class_='cell-aisle-label').get_text().strip() \
        if listing.find('div', class_='cell-aisle-label') else None

    # Find price if applicable and strip dollar sign using regex
    price = listing.find('div', class_='product-prices').find(attrs={"data-test": "amount"}).get_text().strip() \
        if listing.find('div', class_='product-prices').find(attrs={"data-test": "amount"}) else None
    price = re.sub('[^0-9,.]', '', price) if price else None

    # If we have a valid item, write it to the CSV file
    if title:
        propertyWriter.writerow([title, size, aisle, price])


# ----------------------- Web Scraping -----------------------

filename = 'grocery_list.csv'

try :
    print('>>> Starting scraper')
    # Open CSV File
    csvfile = open(filename, 'w', newline='')

    # Set CSV write options
    propertyWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

    # Write header row to CSV
    propertyWriter.writerow(['Title','Size', 'Aisle','Price'])

    # Scrape each page of results and save
    scrape_pages('https://grocery.com/')

except:
  print(">>> Something went wrong")

finally:
    # Close CSV file
    csvfile.close()
    print('>>> All finished!')





