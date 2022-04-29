import scrapy
import json
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from insta.items import InstaItem
# import requests
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError as dke


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = '+79626221370'
    inst_passw = '#PWD_INSTAGRAM_BROWSER:10:1651117313:ASFQANe2nVLBunm1RujmkdJJ5yax0x4qImvPRpWcr1vSU048bYYq7gQ6ZYAZlfCGb3yYaAKJUGk/0GyPt9va/hAeGt2ViaasKZw2O2UKAhHWYtrmGCI9liZF52MHE6H3L8w0XPH5sTp0kxCLrDZA+Di2Jw=='
    user_for_pase = 'techskills_2022'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        # next_page = response.xpath("//a[@class='next i-next']/@href").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
        # links = response.xpath("//a[@class='product-card__name ga-product-card-name']/@href").getall()
        # for link in links:
        #     # print(self.fix_url+link)
        #     yield response.follow(link, callback=self.parse_ads)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_passw},
                                 headers={'X-CSRFToken': csrf_token})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.user_for_pase}',
                                  callback=self.user_parse,
                                  cb_kwargs={'username': self.user_for_pase})

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        # url = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        # url = 'https://i.instagram.com/api/v1/friendships/7709057810/followers/'
        #       # 'count=12&search_surface=follow_list_page'
        url = 'https://i.instagram.com/api/v1/friendships/7709057810/followers/?count=12&search_surface=follow_list_page'
        print()
        max_id = 0
        yield response.follow(url,
                              callback=self.user_posts_parse,
                              cb_kwargs={'max_id': max_id}
                              )

    def user_posts_parse(self, response: HtmlResponse, max_id):
        try:
            j_data = response.json()
        except Exception:
            print()
        item = InstaItem(
            _id=max_id,
            post_data=j_data
        )
        max_id = j_data['next_max_id']
        url = f'https://i.instagram.com/api/v1/friendships/7709057810/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'

        try:
            yield response.follow(url, callback=self.user_posts_parse,
                                  cb_kwargs={'max_id': max_id}
                                  )
        except Exception as e:
            print(e)
            print()

        client = MongoClient('localhost', 27017)
        db = client['friends']
        friend = db.friend
        try:
            friend.insert_one(item)
        except dke:
            pass

        # page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        # if page_info.get('has_next_page'):
        #     variables['after'] = page_info.get('end_cursor')
        #
        #     url = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        #
        #     yield response.follow(url,
        #                           callback=self.user_posts_parse,
        #                           cb_kwargs={'username': username,
        #                                      'user_id': user_id,
        #                                      'variables': deepcopy(variables)})
        #
        # posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        # for post in posts:
        #     item = InstaItem(
        #         user_id=user_id,
        #         username=username,
        #         photo=post.get('node').get('display_url'),
        #         likes=post.get('node').get('edge_media_preview_like').get('count'),
        #         post_data=post.get('node')
        #     )
        #     yield item

        # product.add_xpath('product_specifications_names', "//dl[@class='def-list']/dd/text()")
        # product.add_xpath('product_specifications_values', "//dl[@class='def-list']/dt/text()")

    def fetch_csrf_token(self, text):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
