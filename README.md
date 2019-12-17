# ragnarok-prices

A repository to scrap prices on ragnarok online ragial website.

## How to run the program

Run these commands on your shell:
```
# Install dependencies
pip install -r requirements.txt

# Scrap historical data of all items being sold right now.
scrapy runspider src/scrapper.py -o sales.json

# Plot historical prices of item ITEM_ID. You can pick one randomly from the json file generated.
python src/plot_historical_prices.py --market-data-file sales.json --item-id {ITEM_ID}
```
