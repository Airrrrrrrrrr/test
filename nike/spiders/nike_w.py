import scrapy
import json
import os
from scrapy.cmdline import execute
from nike.items import NikeItem  # 导入 Item 类

class NikeWSpider(scrapy.Spider):
    name = "nike_w"
    url = "https://api.nike.com.cn/cic/browse/v2?queryid=products&anonymousId=DSWXFDD9F68D374125AF2BD522CFDF2233E2&country=cn&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(CN)%26filter%3Dlanguage(zh-Hans)%26filter%3DemployeePrice(true)%26anchor%3D{i}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=zh-Hans&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D"
    start_urls = []
    for i in range(0, 48, 24):
        start_url = url.format(i=i)
        start_urls.append(start_url)

    def parse(self, response):
        data = json.loads(response.text)
        objs = data['data']['products']['products'] # 拿到商品的信息列表，但不包括size和sku
        for obj in objs:
            item = NikeItem()
            item['title'] = obj['subtitle']
            item['price'] = obj['price']
            item['colorways'] = []
            item['size'] = []
            item['sku'] = []

            for color in obj['colorways']: # 可能有多个颜色，遍历获取每个颜色以及详情大图的url
                colorways = {
                    "colorDescription": color['colorDescription'],
                    "img_url": color['images'],
                }
                item['colorways'].append(colorways)

            url = obj['url'].replace('{countryLang}', 'https://www.nike.com.cn/')
            api_key = os.path.split(url)[0].split('-')[-1]
            new_url = 'https://api.nike.com.cn/discover/product_details_availability/v1/marketplace/CN/language/zh-Hans/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647/groupKey/' + api_key
            yield scrapy.Request(new_url, callback=self.parse_size_sku, meta={'item': item})

    def parse_size_sku(self, response):
        item = response.meta['item']
        data = json.loads(response.text)

        for size_info in data.get('sizes', []):
            size_label = size_info.get('localizedLabel', '')
            sku_id = size_info.get('merchSkuId', '')
            if size_label and sku_id:
                item['size'].append(size_label)
                item['sku'].append(sku_id)

        yield item
