# models.py
from .exceptions import OrderNotFoundError


parcel_orders = []


class ParcelOrderStore:
    """Object to store parcel orders."""
    def __init__(self):
        self.db = parcel_orders

    def save(self, sender, recipient, pickup, destination, weight):
        """Save a new order to the store."""
        payload = {
            "id": len(self.db) + 1,
            "sender": sender,
            "recipient": recipient,
            "pickup": pickup,
            "destination": destination,
            "weight": weight
        }
        self.db.append(payload)
        return payload

    def all(self):
        """Return all the orders in the store."""
        return self.db

    def fetch_by_id(self, order_id):
        """Return a specific order by id."""
        try:
            return self.db[order_id - 1]
        except IndexError:
            raise OrderNotFoundError
