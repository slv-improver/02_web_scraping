from functions import *
import os

from datetime import datetime

print(datetime.now().strftime("%H:%M:%S"))

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
	product_data = []
	for page_url in product_urls:
		page_content = get_page_content(page_url)
		product_information = extract_data(page_content, category_title)
		product_information.insert(0, page_url)
		product_data.append(product_information)

	###
	# Export data to csv file
	###
	data_to_csv(product_data, category_title)

print(datetime.now().strftime("%H:%M:%S"))
