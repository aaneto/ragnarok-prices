import json
from datetime import datetime

import click
from matplotlib import dates, pyplot

from sale import StoreSale


@click.command()
@click.option("--market-data-file", help="The file with the ragnarok market data.")
@click.option("--item-id", help="The item id to track.")
def analyze_market_data(market_data_file, item_id):
    with open(market_data_file) as fp:
        market_data = json.load(fp)
        sales = []
        for entry in market_data:
            # this is a 'historical data' entry
            if 'sale_date' in entry and entry['item_id'] == item_id:
                sale = StoreSale.from_dict(entry)
                sales.append(sale)
    sales.sort()
    datetimes = [sale.sale_date for sale in sales]
    prices = [int(sale.price) / 1_000_000 for sale in sales]

    pyplot.plot(datetimes, prices)
    pyplot.ylabel("Million Zenies")
    pyplot.show()


if __name__ == '__main__':
    analyze_market_data()
