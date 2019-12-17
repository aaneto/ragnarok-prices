import scrapy
import json
from sale import BestSale, StoreSale


VENDING_URL = 'http://ragial.org/vending/iRO-Renewal'


class VendingScraper(scrapy.Spider):
    name = 'vending'
    start_urls = [VENDING_URL]
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1
    }

    def parse(self, response):
        # The data extracted from the table is simply the lowest price on sale.
        for item in response.css('tr'):
            item_json = item.css('.itemdb::attr("data-itemdb")').get()
            if item_json:
                item_id = json.loads(item_json)["item"]
                name = item.css('.activate_tr::text').get()
                price = item.css('.price a::text').get()
                sale = BestSale(item_id, name, price)

                yield sale.as_dict()
                yield scrapy.Request(url=sale.get_item_url(
                    1), callback=self.scrap_historical_prices, cb_kwargs=dict(sale=sale))

        next_page = response.css('.next a::attr("href")').get()

        if next_page:
            yield scrapy.Request(url=next_page)

    def scrap_historical_prices(self, response, sale):
        for item in response.css('tr'):
            seller_name = item.css('.name a::text').get()
            sale_date_string = item.css('.date::text').get()
            offered_amount = item.css('.amt::text').get()
            offered_price = item.css('.price a::text').get()
            if offered_price and offered_amount and sale_date_string and seller_name:
                store_sale = StoreSale(
                    sale.id, sale.name, seller_name, sale_date_string, offered_amount, offered_price)

                yield store_sale.as_dict()

        next_page = response.css('.next a::attr("href")').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.scrap_historical_prices, cb_kwargs=dict(sale=sale))
