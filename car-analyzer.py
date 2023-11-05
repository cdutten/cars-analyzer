import logging
import requests
from bs4 import BeautifulSoup
import re
from http.server import BaseHTTPRequestHandler, HTTPServer


# Create a function that takes a url and returns a dictionary with the data we have collected
def get_car_data(url):
    raw_html = requests.get(url)
    soup = BeautifulSoup(raw_html.content, 'html.parser')

    price_html = soup.find_all(name='span', attrs={'class': re.compile('PriceInfo_price__.*')})
    price = price_html[0].text
    price = price[2:-2]
    price = float(price.replace(',', ''))

    mileage_html = soup.find(name='dt', string='Mileage').find_next_sibling('dd').text
    mileage_html = mileage_html.replace('km', '')
    mileage_html = mileage_html.replace(',', '')
    mileage_html = int(mileage_html)

    first_registration_html = soup.find(name='div', string='First registration') \
        .find_next_sibling('div') \
        .find_next_sibling('div').text
    make_model_html = soup.find(name='div', attrs={'class': re.compile('StageTitle_makeModelContainer__.*')})
    make = make_model_html.find_all('span')[0].text
    model = make_model_html.find_all('span')[1].text

    # Find with soup the A tag with the class LocationWithPin_locationItem__.* and get the text
    location_html = soup.find(name='a', attrs={'class': re.compile('LocationWithPin_locationItem__.*')})
    location = location_html.text

    return {
        'price': price,
        'mileage': mileage_html,
        'first_registration': first_registration_html,
        'make': make,
        'model': model,
        'location': location,
        'url': url
    }


# import logging
logging.basicConfig(level=logging.DEBUG)

# Get the data from the cars
cars_to_analyze = [
    'https://www.autoscout24.com/offers/audi-a5-coupe-3-2-fsi-quattro-s-line-plus-xenon-b-o-gasoline-black-e6193db6-e5a4-4ef3-a179-8a73a93fec2b?ipc=recommendation&ipl=homepage-bestresult-listings&position=1&source_otp=t10&source=homepage_last-search',
    'https://www.autoscout24.com/offers/mercedes-benz-cls-350-7g-tronic-gasoline-silver-c1b46f5f-d7a6-4a63-88ec-cb5baf02413c?ipc=recommendation&ipl=homepage-engine-itemBased&position=3&source_otp=nfm&source=homepage_recommender'
]
for car in cars_to_analyze:
    get_car_data(car)

# start http server for prometheus
