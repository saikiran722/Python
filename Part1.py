import requests
from bs4 import BeautifulSoup

def scrape_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})
    for listing in listings:
        product_name_elem = listing.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"

        product_price_elem = listing.find('span', {'class': 'a-offscreen'})
        product_price = product_price_elem.text.strip() if product_price_elem else "N/A"

        rating_elem = listing.find('span', {'class': 'a-icon-alt'})
        rating = rating_elem.text.strip().split(' ')[0] if rating_elem else "N/A"

        num_reviews_elem = listing.find('span', {'class': 'a-size-base'})
        num_reviews = num_reviews_elem.text.strip() if num_reviews_elem else "N/A"

        product_url_elem = listing.find('a', {'class': 'a-link-normal a-text-normal'})
        product_url = "https://www.amazon.in" + product_url_elem.get("href") if product_url_elem else "N/A"

        product = {
            'url': product_url,
            'name': product_name,
            'price': product_price,
            'rating': rating,
            'reviews': num_reviews
        }
        products.append(product) 
    return products

def scrape_multiple_pages(base_url, num_pages):
    all_products = []
    for page in range(1, num_pages + 1):
        page_url = base_url + f'&page={page}'
        products = scrape_page(page_url)
        all_products.extend(products)
    return all_products

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
num_pages = 20
products = scrape_multiple_pages(base_url, num_pages)
for product in products:
    print('Product URL:', product['url'])
    print('Product Name:', product['name'])
    print('Product Price:', product['price'])
    print('Rating:', product['rating'])
    print('Number of Reviews:', product['reviews'])
    print()