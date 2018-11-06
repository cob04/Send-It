# models.py

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
        print(self.db)
        return payload

    def all(self):
        """Return all the orders in the store."""
        return self.db
