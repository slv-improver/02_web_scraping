import requests
from bs4 import BeautifulSoup
import csv
import os
import random

SITE_URL = 'http://books.toscrape.com/'
DATA_DIRECTORY = os.path.join('.', 'data')
BOOKS_DIRECTORY = os.path.join(DATA_DIRECTORY, 'books')
IMAGES_DIRECTORY = os.path.join(DATA_DIRECTORY, 'images')


def get_page_content(url):
	""" Get HTML content

	Parameters:
		url (string): URL of the web page

	Returns:
		bs4.BeautifulSoup: Parsed HTML content as BeautifulSoup Object

	"""
	# Get page content
	page = requests.get(url)
	# Convert page to Object
	return BeautifulSoup(page.content, 'html.parser')


def get_categories(soup):
	""" Get the category titles & URLs

	Parameters:
		soup (bs4.BeautifulSoup): Parsed HTML content as BeautifulSoup Object from get_page_content()

	Returns:
		list: Formatted like [[title, url], [title, url], ...]

	"""
	a_list = soup.find(class_='nav-list').find('ul').find_all('a')
	list_title_and_url = []
	for a in a_list:
		# Text without whitespace & relative category URL formatted
		list_title_and_url.append([a.text.strip(), SITE_URL + a['href']])
	return list_title_and_url


def get_product_page_url(soup, url):
	""" Get the product page URLs of the entire category page.
	If there is pagination, it gets the next page and so on.

	Parameters:
		soup (bs4.BeautifulSoup): Category page content
		url (string): URL of the category page

	Returns:
		list: Books URL

	"""
	# Get parents elements
	div_list = soup.find_all(class_='image_container')
	books_url = []
	# Get URL & format it from relative to absolute
	for div in div_list:
		product_relative_url = div.find('a')['href']
		product_url_list = product_relative_url.split('/')[3:]
		product_url = SITE_URL + 'catalogue/' + '/'.join(product_url_list)
		books_url.append(product_url)
	# Check if there is next page
	try:
		next_page = soup.find(class_='pager').find(class_='next').find('a')['href']
	except AttributeError:
		next_page = ''
	if next_page:
		# Format URL by adding next_page
		url_in_list = url.split('/')[:-1]
		next_page_url = '/'.join(url_in_list) + '/' + next_page
		books_url += get_product_page_url(get_page_content(next_page_url), next_page_url)
	return books_url


def download_image(url, file_name, category):
	""" Download image and save it locally.

	Parameters:
		url: Image URL
		file_name: To rename the image
		category: Category name to create separate folder

	Returns:
		None

	"""
	# Get file extension
	image_extension = '.' + url.split('.')[-1]
	# Get image content in bytes
	image = requests.get(url).content

	# Replace '/' or '\' to write it into the system
	if os.sep in file_name:
		file_name = file_name.replace(os.sep, ' - ')
	destination = IMAGES_DIRECTORY + os.sep + category + os.sep
	path = destination + file_name + image_extension
	# Check if file_name is in th directory & redirect output to /dev/null
	command = 'ls "' + path + '" &> /dev/null'
	if os.system(command) != 512:
		# Change file_name
		number = ''
		# Generate 3 random digit to add them to file_name
		for i in range(3):
			number += str(random.randint(0, 9))
		file_name += number
		path = destination + file_name + image_extension

	# Open new file in "write byte" mode
	with open(path, 'wb') as file:
		file.write(image)


def extract_data(soup, book_category):
	""" Try to extract all data. If nothing there, assign default value.

	Parameters:
		soup (bs4.BeautifulSoup): Product page content
		book_category (string): Category name for assign category

	Returns:
		list: All needed information

	"""
	default_value = 'No Value'
	# Get next td node after element
	try:
		universal_product_code = soup.find(text='UPC').findNext('td').string
	except AttributeError:
		universal_product_code = default_value

	# Get first h1
	try:
		title = soup.h1.string
	except AttributeError:
		title = default_value

	# Get next td node after element
	try:
		price_including_tax = soup.find(text='Price (incl. tax)').findNext('td').string
	except AttributeError:
		price_including_tax = default_value

	# Get next td node after element
	try:
		price_excluding_tax = soup.find(text='Price (excl. tax)').findNext('td').string
	except AttributeError:
		price_excluding_tax = default_value

	# Get next td node after element
	try:
		number_available_text = soup.find(text='Availability').findNext('td').string
		# Extract number from text
		number = ''
		for letter in number_available_text:
			if letter.isdigit():
				number += letter
		number_available = int(number)
	except AttributeError:
		number_available = default_value

	# Get next p node after element
	try:
		product_description = soup.find(id='product_description').findNext('p').string
	except AttributeError:
		product_description = default_value

	# Get next td node after element
	try:
		category = book_category
	except AttributeError:
		category = default_value

	# Get child who has "star-rating" class within "product_main" class element
	try:
		star_rating = soup.find(class_='product_main').find(class_='star-rating')
		# Get its second class name which is the number of stars
		number_of_stars = star_rating['class'][1]
		# Use dictionary to get number
		equivalent = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
		review_rating = equivalent[number_of_stars]
	except AttributeError:
		review_rating = default_value

	# Get src attribute of first img
	try:
		img_relative_url = soup.img['src']
		# Remove relative elements from path
		img_url_list = img_relative_url.split('/')[2:]
		# Create absolute URL
		image_url = SITE_URL + '/'.join(img_url_list)

		download_image(image_url, title, category)
	except AttributeError:
		image_url = default_value

	return {
		'universal_product_code': universal_product_code,
		'title': title,
		'price_including_tax': price_including_tax,
		'price_excluding_tax': price_excluding_tax,
		'number_available': number_available,
		'product_description': product_description,
		'category': category,
		'review_rating': review_rating,
		'image_url': image_url
	}


def data_to_csv(data_list, title):
	""" Extract data from list of products & write them into csv.

	Parameters:
		data_list: List of dict as [{key: 'info', ...}, {key: 'info', ...}, {key: 'info', ...}, {key: 'info', ...}]
		title: Category_name.csv

	Returns:
		None

	"""
	file_name = title + '.csv'
	# Open file to write on it
	with open(BOOKS_DIRECTORY + os.sep + file_name, 'w') as file_csv:
		# Create writer Object
		writer = csv.writer(file_csv, delimiter=',')
		# Write data keys as header
		header = [*data_list[0]]
		writer.writerow(header)
		# Write data values as content
		for product in data_list:
			line = product.values()
			writer.writerow(line)
