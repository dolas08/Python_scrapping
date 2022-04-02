import requests

url = "https://leroymerlin.ru/product/pled-inspire-flamingo-200x220-sm-mikrofibra-cvet-kremovyy-89162747/"
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
search = "обои"
url_2 = f"https://leroymerlin.ru/search/?q={search}"
response = requests.get(url, headers=headers)
response_2 = requests.get(url_2, headers=headers)

print