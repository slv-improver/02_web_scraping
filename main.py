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
