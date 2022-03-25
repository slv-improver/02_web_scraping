import requests
from bs4 import BeautifulSoup
import csv

# Variables
site_url = 'http://books.toscrape.com/'
product_page_url = 'http://books.toscrape.com/catalogue/the-wild-robot_288/index.html'


def url_to_soup_object(url):
	# Get page content
	page = requests.get(url)
	page_content = page.content

	# Convert page to Object
	return BeautifulSoup(page_content, 'html.parser')


def extract_data(soup_object):
	###
	# Extract all needed information
	###

	# Get next td node after element
	universal_product_code = soup_object.find(text='UPC').findNext('td').string

	# Get first h1
	title = soup_object.h1.string

	# Get next td node after element
	price_including_tax = soup_object.find(text='Price (incl. tax)').findNext('td').string

	# Get next td node after element
	price_excluding_tax = soup_object.find(text='Price (excl. tax)').findNext('td').string

	# Get next td node after element
	number_available_text = soup_object.find(text='Availability').findNext('td').string
	# Extract number from text
	number = ''
	for letter in number_available_text:
		if letter.isdigit():
			number += letter
	number_available = int(number)

	# Get next p node after element
	product_description = soup_object.find(id='product_description').findNext('p').string

	# Get next td node after element
	category = soup_object.find(text='Product Type').findNext('td').string

	# Get child who has "star-rating" class within "product_main" class element
	star_rating = soup_object.find(class_='product_main').find(class_='star-rating')
	# Get its second class name which is the number of stars
	number_of_stars = star_rating['class'][1]
	# Use dictionary to get number
	equivalent = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
	review_rating = equivalent[number_of_stars]

	# Get src attribute of first img
	image_relative_url = soup_object.img['src']
	# Remove relative elements from path
	image_url_list = image_relative_url.split('/')[2:]
	# Create absolute URL
	image_url = site_url + '/'.join(image_url_list)

	return [
		universal_product_code,
		title, price_including_tax,
		price_excluding_tax,
		number_available,
		product_description,
		category,
		review_rating,
		image_url
	]


soup = url_to_soup_object(product_page_url)


###
# Export data to csv file
###

file_header = [
	'product_page_url',
	'universal_product_code',
	'title',
	'price_including_tax',
	'price_excluding_tax',
	'number_available',
	'product_description',
	'category',
	'review_rating',
	'image_url'
]
file_line = extract_data(soup)

file_name = 'category.csv'
with open('books/' + file_name, 'w') as file_csv:
	writer = csv.writer(file_csv, delimiter=',')
	writer.writerow(file_header)
	writer.writerow(file_line)
