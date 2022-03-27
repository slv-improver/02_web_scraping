from functions import *
import os

from datetime import datetime

print(datetime.now().strftime("%H:%M:%S"))

# Remove all data before starting to get only the newer information
os.system('rm -rf ' + DATA_DIRECTORY)

# Get page content
site_soup = get_page_content(SITE_URL)
# Get category list URL
categories = get_categories(site_soup)

# Create books destination directory
os.makedirs(BOOKS_DIRECTORY, exist_ok=True)

for category in categories:
	# Assign title and URL
	category_title = category[0].lower()
	category_url = category[1]

	# Create images destination directory
	destination = IMAGES_DIRECTORY + os.sep + category_title
	os.makedirs(destination, exist_ok=True)

	# Get list of product page URL from category page
	category_page_content = get_page_content(category_url)
	product_urls = get_product_page_url(category_page_content, category_url)
	product_data_list = []
	for url in product_urls:
		page_content = get_page_content(url)
		# Get single product information
		product_info = extract_data(page_content, category_title)
		product_info['product_page_url'] = url
		# Add product info to list of multiple product information
		product_data_list.append(product_info)
		# [{key: 'info', ...}, {key: 'info', ...}, {key: 'info', ...}, {key: 'info', ...}]

	###
	# Export data to csv file
	###
	data_to_csv(product_data_list, category_title)

print(datetime.now().strftime("%H:%M:%S"))
