# Я выбрал Twitch в качестве цели к домашнему заданию
# в документации я нашёл всё, что нужно чтобы сделать свой первый запрос
# зарегистрировал своё приложение, установил twitch-cli, power shell 7, scoop
# получил свой токен, который мне предложили использовать в Curl.(тоже установил)
# после получения токена мне предложили использовать запрос в Curl, но мне необходимо сделать такой запрос в Python.
# curl -X GET 'https://api.twitch.tv/helix/users?login=twitchdev' \
# -H 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx' \
# -H 'Client-Id: wbmytr93xzw8zbg0p1izqyzzc5mbiz'
# чуть покапался в Curl, -H это заголовки, осталось их найти их аналог в requests.
# наткнулся на конвертер curl запроса в python код, какая удача
# https://reqbin.com/req/c-w7oitglz/convert-curl-to-http-request
# осталось подставить свои значения, потому что я конвертировал запрос написанный в документации
import requests
from pprint import pprint
import json
# from requests.structures import CaseInsensitiveDict  # изначально headers = dict был  headers = CaseInsensitiveDict()
# но это оказалось ненужно, просто проверив обычный dict()

url = "https://api.twitch.tv/helix/users?login=twitchdev"

headers = dict()
# в случае с twitch Authorizations = app access token
# а так же необходимо писать Bearer
headers["Authorization"] = "Bearer s8hc6pqyyoyu4lchfyy9o5ra8npuwd"
headers["Client-Id"] = "297ln470xsguucw9es2tp6tt517vez"

resp = requests.get(url, headers=headers)
j_data = resp.json()
pprint(j_data)

with open('response.json', 'w', encoding='utf-8') as f:
    json.dump(j_data, f, ensure_ascii=False, indent=4)
