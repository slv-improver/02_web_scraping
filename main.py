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
universal_product_code = soup.find(text='UPC').findNext('td').string

# Get first h1
title = soup.h1.string

# Get next td node after element
price_including_tax = soup.find(text='Price (incl. tax)').findNext('td').string

# Get next td node after element
price_excluding_tax = soup.find(text='Price (excl. tax)').findNext('td').string

# Get next td node after element
number_available_text = soup.find(text='Availability').findNext('td').string
# Extract number from text
number = ''
for letter in number_available_text:
	if letter.isdigit():
		number += letter
number_available = int(number)

# Get next p node after element
product_description = soup.find(id='product_description').findNext('p').string

# Get next td node after element
category = soup.find(text='Product Type').findNext('td').string

# Get child who has "star-rating" class within "product_main" class element
star_rating = soup.find(class_='product_main').find(class_='star-rating')
# Get its second class name which is the number of stars
number_of_stars = star_rating['class'][1]
# Use dictionary to get number
equivalent = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
review_rating = equivalent[number_of_stars]

# Get src attribute of first img
image_relative_url = soup.img['src']
# Remove relative elements from path
image_url_list = image_relative_url.split('/')[2:]
# Create absolute URL
image_url = site_url + '/'.join(image_url_list)
