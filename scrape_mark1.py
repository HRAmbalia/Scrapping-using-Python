## DONE

import requests
from bs4 import BeautifulSoup
import pandas as pd
from .config import api_key_scrapeops

#searchTag = input('Enter serach Tag : ')
searchTag = 'Bags'

items = []
response = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': api_key_scrapeops,
        'url': 'https://www.amazon.in/s?k=' + searchTag, 
    },
)
htmlContent = response.content
soup = BeautifulSoup(htmlContent, 'html5lib')
results = soup.find_all('div', attrs = {'data-component-type':'s-search-result'})

if (len(results)==0):
    exit()

for result in results:
    try:
        ## Product Name
        prod_name = result.h2.text
        print('Product Name : ' + prod_name)

        ## Product URL
        prod_link = ('https://amazon.in' + result.h2.a['href'])
        print('Product Link : ' + prod_link)

        ## Product Price
        prod_price = (result.find('span', {'class': 'a-offscreen'}).text)
        print('Product Price : ' + prod_price)

        ## Product Rating
        prod_rating = (result.find('span', {'class': 'a-icon-alt'}).text)
        print('Product Rating : ' + prod_rating)

        ## No of review
        prod_review = (result.find('span', {'class': 'a-size-base puis-light-weight-text s-link-centralized-style'}).text)
        print('No of Reviews : ' + prod_review)

    except:
        prod_price = prod_rating = prod_review = 'Error'
        print("Got an Error")
        continue

    items.append([prod_name, prod_link, prod_price, prod_rating, prod_review])

df = pd.DataFrame(items, columns=['Product', 'Product URL', 'Product Price', 'Product Rating', 'No of review'])
df.to_csv('{0}.csv'.format(searchTag), index=False)
