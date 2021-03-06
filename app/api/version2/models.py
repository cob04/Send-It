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

    def save(self, user_id, sender, recipient, pickup, destination, weight):
        """Save a new order to the store."""
        payload = {
            "id": len(self.db) + 1,
            "user_id": user_id,
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

    def update_by_id(self, order_id, user_id, sender, recipient, pickup,
                     destination, weight, status):
        """Save a new order to the store."""
        order = self.fetch_by_id(order_id)
        order["user_id"] = user_id
        order["sender"] = sender
        order["recipient"] = recipient
        order["pickup"] = pickup
        order["destination"] = destination
        order["weight"] = weight
        order["status"] = status
        self.db[order["id"] - 1] = order
        return self.db[order["id"] - 1]

    def fetch_by_user_id(self, user_id):
        """Return all orders of a specific user."""
        orders = [order for order in self.all() if order["user_id"] == user_id]
        return orders


LOGGED_IN = "logged in"
LOGGED_OUT = "logged out"


user_data = []


class UserDataStore:
    """Object to store user data."""
    def __init__(self):
        self.db = user_data

    def save(self, name, email, password):
        """Save a new user to the store."""
        for user in self.db:
            if user["email"] == email:
                return {"error": "Email address already in use"}

        new_user = {
            "id": len(self.db) + 1,
            "name": name,
            "email": email,
            "password": password,
            "login_status": LOGGED_OUT
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

    def fetch_by_id(self, user_id):
        """Return the user specified by id."""
        user = self.db[user_id - 1]
        payload = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
        return payload

    def login_user(self, email, password):
        """Login in a user by marking the store."""
        if self.authenticate(email, password):
            for user in self.db:
                if user["email"] == email:
                    user["login_status"] = LOGGED_IN
                    return {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                        "login_status": user["login_status"]
                    }
        return {"error": "Invalid Credentials"}

    def logout_user(self, email):
        """logout a user by marking the store."""
        for user in self.db:
            if user["email"] == email and user["login_status"] == LOGGED_IN:
                user["login_status"] = LOGGED_OUT
                return {"message": "You have been successfully logged out."}
            else:
                return {
                    "message": "Your email is invalid or you"
                             " are already logged out."
                }
