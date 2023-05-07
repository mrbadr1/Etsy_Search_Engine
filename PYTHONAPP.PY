import requests

api_key = 'qwoxgbhbzzbu46ukllrzmqc0'
shop_name = '1430607176'
url = f'https://api.etsy.com/v3/application/shops/{shop_name}/listings/active'

headers = {
    'x-api-key': api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    listings = response.json()
    for listing in listings['results']:
        print(f"Listing ID: {listing['listing_id']}, Title: {listing['title']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
