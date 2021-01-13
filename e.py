import requests
from requests_html import HTMLSession

url = "https://www.yelp.com/biz/j-and-m-construction-services-dover"

try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(response.text)
except requests.exceptions.RequestException as e:
    print(e)
