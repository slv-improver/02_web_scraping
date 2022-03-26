import csv
from functions import *

from datetime import datetime

print(datetime.now().strftime("%H:%M:%S"))

# Get page content
site_soup = get_page_content(SITE_URL)
# Get category list URL
category_list = get_categories(site_soup)

for category_item in category_list:
	category_title = category_item[0]
	category_url = category_item[1]
	# Get list of product page URL
	category_page_soup = get_page_content(category_url)
	product_page_list = get_product_page_url(category_page_soup, category_url)
	information_list = []
	for page_url in product_page_list:
		page_content = get_page_content(page_url)
		product_information = extract_data(page_content, category_title)
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

print(datetime.now().strftime("%H:%M:%S"))
