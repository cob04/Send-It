import psycopg2

from app.db_config import init_db


class ParcelOrderModel:

    def __init__(self, sender, recipient, pickup, destination, weight,
                 parcel_id=None):
        self.id = parcel_id
        self.sender = sender
        self.recipient = recipient
        self.pickup = pickup
        self.destination = destination
        self.weight = weight

    def __repr__(self):
        return "Parcel(%s, %s, %s, %s, %sKg)" % (self.sender,
                                                 self.recipient,
                                                 self.pickup,
                                                 self.destination,
                                                 self.weight)


class ParcelOrderManager:

    def __init__(self):
        self.db = init_db()

    def save(self, parcel):
        """Insert parcel order data to the database."""
        query = """ INSERT INTO parcels (sender, recipient, pickup, destination,
                weight) VALUES (%s, %s, %s, %s, %s)"""
        new_record = (parcel.sender, parcel.recipient, parcel.pickup,
                      parcel.destination, parcel.weight)
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
                parcel_id, *other_fields = row
                data.append(ParcelOrderModel(*other_fields,
                                             parcel_id=parcel_id))
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
            parcels = cursor.fetchall()
            data = []
            for row in parcels:
                parcel_id, *fields = row
                data.append(ParcelOrderModel(*fields, parcel_id=parcel_id))
            return data[0]

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error fetching parcel", error

        finally:
            cursor.close()
