import requests
from bs4 import BeautifulSoup

def scrape_product_page(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find('div', {'id': 'feature-bullets'}).find('ul').text.strip()
    ASIN = soup.find('th', text='ASIN').find_next('td').text.strip()
    product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
    manufacturer = soup.find('div', {'id': 'bylineInfo'}).text.strip()

    additional_details = {
        'description': description,
        'ASIN': ASIN,
        'product_description': product_description,
        'manufacturer': manufacturer
    }

    return additional_details

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

response = requests.get(base_url)

soup = BeautifulSoup(response.content, 'html.parser')

listings = soup.find_all('div', {'data-component-type': 's-search-result'})

products = []

for listing in listings:
    product_url = 'https://www.amazon.in' + listing.find('a', {'class': 'a-link-normal s-no-outline'})['href']
    product_name = listing.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
    product_price = listing.find('span', {'class': 'a-offscreen'}).text.strip()
    rating = listing.find('span', {'class': 'a-icon-alt'}).text.strip().split(' ')[0]
    num_reviews = listing.find('span', {'class': 'a-size-base'}).text.strip()

    additional_details = scrape_product_page(product_url)

    product = {
        'url': product_url,
        'name': product_name,
        'price': product_price,
        'rating': rating,
        'reviews': num_reviews,
        'description': additional_details['description'],
        'ASIN': additional_details['ASIN'],
        'product_description': additional_details['product_description'],
        'manufacturer': additional_details['manufacturer']
    }

    products.append(product)

for product in products:
    print('Product URL:', product['url'])
    print('Product Name:', product['name'])
    print('Product Price:', product['price'])
    print('Rating:', product['rating'])
    print('Number of Reviews:', product['reviews'])
    print('Description:', product['description'])
    print('ASIN:', product['ASIN'])
    print('Product Description:', product['product_description'])
    print('Manufacturer:', product['manufacturer'])
    print()