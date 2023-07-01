# Import libraries
from bs4 import BeautifulSoup
import requests
import re

search_term = input("What properties do you want to search for? ")

# Specific URL to scrape
url = 'https://batdongsan24h.com.vn/bat-dong-san-ban-tai-viet-nam-s32113/-1/-1/-1'

# Make HTTP request and create BeautifulSoup object
response = requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')

# Extract data using BeautifulSoup selectors
properties_text = soup.find(class_='center-body')
properties = int(str(properties_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

# Loop through the extracted data and print the results
for property in range(1, properties + 1): 
    url = 'https://batdongsan24h.com.vn/bat-dong-san-ban-tai-viet-nam-s32113/-1/-1/-1/page={page}'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    
    property_name = property.find(class_='sieu-vip-title')
    image = property.find(class_='box-img-thumb')
    prices = property.find(class_='price-list') 
    acreage = property.find(class_='price-list')
    location = property.find(class_='price-list')
    published_time = property.find(class_='pull-right time')
    
    div = properties.find(class_="item-re-list clearfix")
    items = div.find_all(text=re.compile(search_term))

    for item in items:
	        parent = item.parent
            if parent.name != "a":
                continue

            link = parent['href']
            next_parent = item.find_parent(class_="item-container")
            try:
                price = next_parent.find(class_="price-current").find("strong").string
                items_found[item] = {"price": int(price.replace(",", "")), "link": link}
            except:
                pass


    print("Title:", property_name)
    print("Thumb_image:", image)
    print("Price:", prices)
    print("Acreage:", acreage)
    print("Location:", location)
    print("Published date:", published_time)
    print("-----")

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])