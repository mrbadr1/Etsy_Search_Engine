from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
ETSY_API_KEY = 'qwoxgbhbzzbu46ukllrzmqc0'
@app.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        num_pages = int(request.form['page'])
        data = []
        for page in range(1, num_pages+1):
         url = f'https://www.etsy.com/search?q={query}&page={page}'
         response = requests.get(url)
         soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the information you want from the HTML using BeautifulSoup
        # and create a list of dictionaries with the data
         for item in soup.find_all('div', {'class': 'v2-listing-card'}):
          title = item.find('h3', {'class': 'wt-text-caption v2-listing-card__title wt-text-truncate'}).text.strip()
          price = item.find('span', {'class': 'currency-value'}).text.strip()
          link = 'https://www.etsy.com' + item.find('a', {'class': 'listing-link'})['href']
          img_url = item.find('img', {'class': 'wt-width-full'})['src']
          data.append({'title': title, 'price': price, 'link': link, 'img_url': img_url})
        return render_template('index.html', data=data)
    return render_template('index.html')
@app.route('/listing_date', methods=['GET','POST'])
def get_listing_date():
    if request.method == 'POST':
        listing_id = request.form['listing_id']
        dataid = []
    if not listing_id:
        return jsonify({'error': 'Please provide a listing_id'}), 400

    url = f'https://openapi.etsy.com/v2/listings/{listing_id}?api_key={ETSY_API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch listing details'}), response.status_code

    listing_data = response.json()
    if 'results' not in listing_data or len(listing_data['results']) == 0:
        return jsonify({'error': 'No listing found'}), 404

    listing = listing_data['results'][0]
    creation_date = listing['creation_tsz']
    print(creation_date)
    print(listing_id)
    dataid={'listing_id': listing_id, 'creation_date': creation_date}
    return render_template('search_date.html', dataid=dataid)

if __name__== "__name__":
    app.run(debug=True)

