from datetime import datetime

ITEM_URL = 'http://ragial.org/item/iRO-Renewal'


class StoreSale:
    """Representation of a store sale."""

    def parse_sale_date(self, sale_date_string):
        """Parse a sale date string into a date."""
        if sale_date_string == "Now":
            return datetime.now().date()

        return datetime.strptime(sale_date_string, '%b-%d-%y').date()

    def __init__(self, item_id, item_name, seller_name, sale_date_string, offered_amount, offered_price):
        self.item_id = item_id
        self.item_name = item_name
        self.seller_name = seller_name
        self.offered_amount = offered_amount.replace(",", "").replace("x", "")
        self.price = offered_price.replace(",", "").replace("z", "")

        try:
            self.sale_date = self.parse_sale_date(sale_date_string)
        except:
            self.sale_date = None

    @classmethod
    def from_dict(cls, entry):
        sale = cls(entry.get('item_id'), entry.get('item_name'), entry.get('seller_name'),
                   "", entry.get('offered_amount'), entry.get('offered_price'))
        sale.sale_date = datetime.strptime(
            entry.get('sale_date'), '%Y-%m-%d').date()

        return sale

    def __eq__(self, other):
        return (
            self.item_id == other.item_id and
            self.seller_name == other.seller_name and
            self.offered_amount == other.offered_amount and
            self.price == other.price and
            self.sale_date == other.sale_date
        )

    def __gt__(self, other):
        return self.sale_date > other.sale_date

    def as_dict(self):
        """Return dict representation of an BestSale."""
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'offered_price': self.price,
            'offered_amount': self.offered_amount,
            'sale_date': self.sale_date,
            'seller_name': self.seller_name
        }


class BestSale:
    """Representation of the best sale of an item happening on Ragnarok."""

    def __init__(self, item_id, name, price):
        self.id = item_id
        self.name = name
        self.price = price.replace(",", "").replace("z", "")

    def get_item_url(self, page):
        return f"{ITEM_URL}/{self.id}/{page}"

    def as_dict(self):
        """Return dict representation of an BestSale."""
        return {
            'item_id': self.id,
            'item_name': self.name,
            'item_price': self.price,
        }
