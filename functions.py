import requests
from bs4 import BeautifulSoup

SITE_URL = 'http://books.toscrape.com/'


def get_page_content(url):
	""" Get HTML content

	Parameters:
		url (string): URL of the web page

	Returns:
		string: parsed HTML content as BeautifulSoup Object

	"""
	# Get page content
	page = requests.get(url)
	# Convert page to Object
	return BeautifulSoup(page.content, 'html.parser')


def get_categories(soup_object):
	""" Get the category titles & URLs

	Parameters:
		soup_object (string): parsed HTML content as BeautifulSoup Object from get_page_content()

	Returns:
		list: formatted like [[title, url], [title, url], ...]

	"""
	a_list = soup_object.find(class_='nav-list').find('ul').find_all('a')
	list_title_and_url = []
	for a in a_list:
		# Text without whitespace & relative category URL formatted
		list_title_and_url.append([a.text.strip(), SITE_URL + a['href']])
	return list_title_and_url


def get_product_page_url(soup_object, url):
	###
	# Get product page URL from category page
	###

	# Get parents elements
	div_list = soup_object.find_all(class_='image_container')
	books_url = []
	# Get URL & format it from relative to absolute
	for div in div_list:
		product_relative_url = div.find('a')['href']
		product_url_list = product_relative_url.split('/')[3:]
		product_url = SITE_URL + 'catalogue/' + '/'.join(product_url_list)
		books_url.append(product_url)
	# Check if there is next page
	try:
		next_page = soup_object.find(class_='pager').find(class_='next').find('a')['href']
	except AttributeError:
		next_page = ''
	if next_page:
		# Format URL by adding next_page
		url_in_list = url.split('/')[:-1]
		next_page_url = '/'.join(url_in_list) + '/' + next_page
		books_url += get_product_page_url(url_to_soup_object(next_page_url), next_page_url)
	# Info
	print('Category')
	###
	return books_url


def extract_data(soup_object, book_category):
	###
	# Extract all needed information
	###

	# Get next td node after element
	try:
		universal_product_code = soup_object.find(text='UPC').findNext('td').string
	except AttributeError:
		universal_product_code = 'No Value'

	# Get first h1
	try:
		title = soup_object.h1.string
	except AttributeError:
		title = 'No Value'

	# Get next td node after element
	try:
		price_including_tax = soup_object.find(text='Price (incl. tax)').findNext('td').string
	except AttributeError:
		price_including_tax = 'No Value'

	# Get next td node after element
	try:
		price_excluding_tax = soup_object.find(text='Price (excl. tax)').findNext('td').string
	except AttributeError:
		price_excluding_tax = 'No Value'

	# Get next td node after element
	try:
		number_available_text = soup_object.find(text='Availability').findNext('td').string
		# Extract number from text
		number = ''
		for letter in number_available_text:
			if letter.isdigit():
				number += letter
		number_available = int(number)
	except AttributeError:
		number_available = 'No Value'

	# Get next p node after element
	try:
		product_description = soup_object.find(id='product_description').findNext('p').string
	except AttributeError:
		product_description = 'No Value'

	# Get next td node after element
	try:
		category = book_category
	except AttributeError:
		category = 'No Value'

	# Get child who has "star-rating" class within "product_main" class element
	try:
		star_rating = soup_object.find(class_='product_main').find(class_='star-rating')
		# Get its second class name which is the number of stars
		number_of_stars = star_rating['class'][1]
		# Use dictionary to get number
		equivalent = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
		review_rating = equivalent[number_of_stars]
	except AttributeError:
		review_rating = 'No Value'

	# Get src attribute of first img
	try:
		image_relative_url = soup_object.img['src']
		# Remove relative elements from path
		image_url_list = image_relative_url.split('/')[2:]
		# Create absolute URL
		image_url = SITE_URL + '/'.join(image_url_list)
	except AttributeError:
		image_url = 'No Value'

	# Info
	print('Product')
	###
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
