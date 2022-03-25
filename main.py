import requests
from bs4 import BeautifulSoup

# Variables
site_url = 'http://books.toscrape.com/'
product_page_url = 'http://books.toscrape.com/catalogue/the-wild-robot_288/index.html'

# Get page content
page = requests.get(product_page_url)
page_content = page.content

# Convert page to Object
soup = BeautifulSoup(page_content, 'html.parser')

###
# Extract all needed information
###

# Get next td node after element
universal_product_code = soup.find(text='UPC').findNext('td')

# Get first h1
title = soup.h1

# Get next td node after element
price_including_tax = soup.find(text='Price (incl. tax)').findNext('td')

# Get next td node after element
price_excluding_tax = soup.find(text='Price (excl. tax)').findNext('td')

# Get next td node after element
number_available_text = soup.find(text='Availability').findNext('td')

# Get next p node after element
product_description = soup.find(id='product_description').findNext('p')

# Get next td node after element
category = soup.find(text='Product Type').findNext('td')

# Get child who has "star-rating" class within "product_main" class element
star_rating = soup.find(class_='product_main').find(class_='star-rating')

# Get src attribute of first img
image_url = soup.img['src']
