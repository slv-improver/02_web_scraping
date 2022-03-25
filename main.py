import requests
from bs4 import BeautifulSoup
import csv

# Variables
site_url = 'http://books.toscrape.com/'


def url_to_soup_object(url):
	# Get page content
	page = requests.get(url)
	page_content = page.content

	# Convert page to Object
	return BeautifulSoup(page_content, 'html.parser')


def get_category_li(soup_object):
	a_list = soup_object.find(class_='nav-list').find('ul').find_all('a')
	list_title_and_url = []
	for a in a_list:
		list_title_and_url.append([a.text.strip(), site_url + a['href']])
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
		product_url = site_url + 'catalogue/' + '/'.join(product_url_list)
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
	return books_url


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


# Get page content
site_soup = url_to_soup_object(site_url)
# Get category list URL
category_list = get_category_li(site_soup)

for category in category_list:
	category_title = category[0]
	category_url = category[1]
	# Get list of product page URL
	category_page_soup = url_to_soup_object(category_url)
	product_page_list = get_product_page_url(category_page_soup, category_url)
	information_list = []
	for page_url in product_page_list:
		page_content = url_to_soup_object(page_url)
		product_information = extract_data(page_content)
		product_information.insert(0, page_url)
		information_list.append(product_information)
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

	file_name = category_title + '.csv'
	# Open file to write on it
	with open('books/' + file_name, 'w') as file_csv:
		# Create writer Object
		writer = csv.writer(file_csv, delimiter=',')
		# Write header & information
		writer.writerow(file_header)
		for information in information_list:
			writer.writerow(information)
