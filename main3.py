# using autoscraper
from autoscraper import AutoScraper
url = 'https://www.amazon.in/s?k=bags'

title = ["Skybags Brat Black 46 Cms Casual Backpack"]
titles = AutoScraper().build(url, title)
print(titles)

no_of_reviews = ["2,558"]
no_of_reviews = AutoScraper().build(url, no_of_reviews)
print(no_of_reviews)

price = ["₹669"]
prices = AutoScraper().build(url, price)
print(prices)


