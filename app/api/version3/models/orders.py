import psycopg2

from app.db_config import init_db


NOT_DELIVERED = "Parcel not delivered"
DELIVERED = "Parcel delivered"
IN_TRANSIT = "Parcel in transit"
CANCELLED = "Parcel cancelled"


class ParcelOrderModel:
    """Object to store parcel data for easy retrival.
    """
    def __init__(self, user_id, sender, recipient, pickup, destination, weight,
                 parcel_id=None, status=None):
        self.id = parcel_id
        self.user_id = user_id
        self.sender = sender
        self.recipient = recipient
        self.pickup = pickup
        self.destination = destination
        self.weight = weight
        if not status:
            self.status = NOT_DELIVERED
        else:
            self.status = status

    def __repr__(self):
        return "Parcel(%s, %s, %s, %s, %sKg)" % (self.sender,
                                                 self.recipient,
                                                 self.pickup,
                                                 self.destination,
                                                 self.weight)

    def to_dict(self):
        """Return a parce in a dictionary format."""
        parcel_dict = {
            "user_id": self.user_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "pickup": self.pickup,
            "destination": self.destination,
            "weight": float(self.weight),
            "status": self.status,
        }
        if self.id:
            parcel_dict["id"] = self.id
        return parcel_dict

    def cancel(self):
        """Mark the parcel as cancelled."""
        self.status = CANCELLED


class ParcelOrderManager:
    """Object to abstract away database interations.
    Does insertions, retrivals and data manipulation.
    """
    def __init__(self):
        self.db = init_db()

    def save(self, parcel):
        """Insert parcel order data to the database."""
        query = """ INSERT INTO parcels (user_id, sender, recipient, pickup, destination,
                weight) VALUES (%s, %s, %s, %s, %s, %s)"""
        new_record = (parcel.user_id, parcel.sender, parcel.recipient,
                      parcel.pickup, parcel.destination, parcel.weight)
        try:
            cursor = self.db.cursor()
            cursor.execute(query, new_record)
            self.db.commit()
            return parcel

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error inserting new parcel", error

        finally:
            cursor.close()

    def fetch_all(self):
        """Fetch all parcels."""
        query = """ SELECT * FROM parcels"""
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            all_parcels = cursor.fetchall()
            data = []
            for row in all_parcels:
                parcel_id, *other_fields, status = row
                data.append(ParcelOrderModel(*other_fields,
                                             parcel_id=parcel_id,
                                             status=status))
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error fetching parcels", error

        finally:
            cursor.close()

    def fetch_by_id(self, parcel_id):
        """Fetch one order by id."""
        query = """ SELECT * FROM parcels where parcel_id = %s"""
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (parcel_id,))
            parcel_id, *fields, status = cursor.fetchone()
            parcel = ParcelOrderModel(*fields, parcel_id, status)
            return parcel

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error fetching parcel", error

        finally:
            cursor.close()

    def cancel_by_id(self, parcel_id):
        """Cancel the parcel of the id provided."""
        select_parcel_query = """ SELECT * FROM parcels WHERE parcel_id = %s;"""
        update_parcel_query = """UPDATE parcels SET status = %s  WHERE parcel_id = %s;"""
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(update_parcel_query, (CANCELLED, parcel_id))
                    self.db.commit()
                    cursor.execute(select_parcel_query, (parcel_id,))
                    parcel_id, *fields, status = cursor.fetchone()
                    parcel = ParcelOrderModel(*fields,
                                              parcel_id=parcel_id,
                                              status=status)
                    return parcel

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error updating parcel", error

    def update_destination(self, parcel_id, destination):
        """Change the parcels destination."""
        select_parcel_query = """ SELECT * FROM parcels WHERE parcel_id = %s;"""
        update_parcel_query = """UPDATE parcels SET destination = %s WHERE parcel_id = %s;"""
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(update_parcel_query, (destination, parcel_id))
                    self.db.commit()
                    cursor.execute(select_parcel_query, (parcel_id,))
                    parcel_id, *fields, status = cursor.fetchone()
                    parcel = ParcelOrderModel(*fields,
                                              parcel_id=parcel_id,
                                              status=status)
                    return parcel

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error updating parcel", error
