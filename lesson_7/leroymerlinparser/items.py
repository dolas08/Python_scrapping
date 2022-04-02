# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def fix_price(price_list):
    temp = ''.join(price_list)
    temp_1 = []
    temp = temp.split()
    if len(temp) == 8:
        temp_1.append(temp[0] + temp[1])
        temp_1.append(temp[2] + ' ' + temp[3])
        temp_1.append(temp[4] + temp[5])
        temp_1.append(temp[6] + ' ' + temp[7])
        end_price_list = []
        end_price_list.append(float(temp_1[0].replace('руб.', '')) / 100)
        end_price_list.append('руб')
        end_price_list.append(temp_1[1])
        end_price_list.append(float(temp_1[2].replace('руб.', '')))
        end_price_list.append('руб. за упаковку')
    else:
        try:
            end_price_list = [float(''.join(temp).replace('руб.', '')), 'руб.']
        except Exception as e:
            print(e)
            return temp
    return end_price_list


def fix_image(image_list):
    temp = []
    for each in image_list:
        if each.find('1800x') > 0:
            temp.append(each)
    return temp


def fix_table(table_list):
    temp = {}
    i = 0
    while i < len(table_list) / 2:
        temp.update({f'{" ".join((table_list[i].split()))}': f'{" ".join(table_list[i + 1].split())}'})
        i += 2
    return temp


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(fix_price))
    photos = scrapy.Field(input_processor=Compose(fix_image))
    table = scrapy.Field(input_processor=Compose(fix_table))
    _id = scrapy.Field()
