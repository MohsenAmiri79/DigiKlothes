import re
import json
import requests

url = "https://www.digikala.com/product/dkp-9115608/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D9%88%D8%A7%D9%86-%D9%BE%D9%84%D8%A7%D8%B3-%D9%85%D8%AF%D9%84-10-pro-%D8%AF%D9%88-%D8%B3%DB%8C%D9%85-%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D9%88-%D8%B1%D9%85-12-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA/"

id_ = re.search(r"-(\d+)/", url).group(1)
product_url = f"https://api.digikala.com/v1/product/{id_}/"
data = requests.get(product_url).json()

print(data['data']['seo']['markup_schema'][0]['image'])