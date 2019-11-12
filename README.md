# ragnarok-prices

A repository to scrap prices on ragnarok online ragial website.

## What does the scrapper.py do?

It downloads all the *live* items on sale on ragial, and then proceeds to download
the historical prices of those items on ragial and save everything into a json file.

## What does the plot_historical_prices do?

Using a json file acquired using scrapper.py, you can plot graphs of a particular item id, to see
how does today compare with most days, when it comes to the item price.
