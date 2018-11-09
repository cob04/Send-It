# models.py

CANCELLED = "Order cancelled"
IN_TRANSIT = "Order in transit"
DELIVERED = "Order delivered"
NOT_DELIVERED = "Order not deliverd"


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
            "weight": weight,
            "status": NOT_DELIVERED
        }
        self.db.append(payload)
        return self.db[payload["id"] - 1]

    def all(self):
        """Return all the orders in the store."""
        return self.db

    def fetch_by_id(self, order_id):
        """Return the order specified by id."""
        return self.db[order_id - 1]

    def cancel_by_id(self, order_id):
        """Mark an order as cancelled."""
        order = self.fetch_by_id(order_id)
        order["status"] = CANCELLED
        return order


user_data = []


class UserDataStore:
    """Object to store user data."""
    def __init__(self):
        self.db = user_data

    def save(self, name, email, password):
        """Save a new user to the store."""
        new_user = {
            "id": len(self.db) + 1,
            "name": name,
            "email": email,
            "password": password
        }
        self.db.append(new_user)
        user = self.db[new_user["id"] - 1]
        payload = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        }
        return payload

    def authenticate(self, email, password):
        """Authenticate users in the store."""
        for user in self.db:
            if user["email"] == email and user["password"] == password:
                return True
        else:
            return False
