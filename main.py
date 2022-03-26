import csv
from functions import *

from datetime import datetime

print(datetime.now().strftime("%H:%M:%S"))

# Get page content
site_soup = get_page_content(SITE_URL)
# Get category list URL
categories = get_categories(site_soup)

for category in categories:
	# Assign title and URL
	category_title = category[0]
	category_url = category[1]
	# Get list of product page URL from category page
	category_page_content = get_page_content(category_url)
	product_urls = get_product_page_url(category_page_content, category_url)
	product_data = []
	for page_url in product_urls:
		page_content = get_page_content(page_url)
		product_information = extract_data(page_content, category_title)
		product_information.insert(0, page_url)
		product_data.append(product_information)

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
		for data in product_data:
			writer.writerow(data)

print(datetime.now().strftime("%H:%M:%S"))
