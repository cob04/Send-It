import psycopg2

from werkzeug.security import  generate_password_hash, check_password_hash

from app.db_config import init_db


ADMIN = "Administrator"
NORMAL = "Normal"


class UserModel:

    def __init__(self, name, email, password, user_id=None, role=None):

        self.id = user_id
        self.name = name
        self.email = email
        self._password = generate_password_hash(password)
        if not role:
            self.role = NORMAL
        else:
            self.role = role

    def __repr__(self):
        return "User(%s, %s, %s,)" % (self.name, self.email, self.role)

    def check_password(self, password):
        """Check if provided password is correct."""
        return check_password_hash(self._password, password)

    def to_dict(self):
        """Return a parce in a dictionary format."""
        user_dict = {
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }
        if self.id:
            user_dict["id"] = self.id
        return user_dict


class UserManager:

    def __init__(self):
        self.db = init_db()

    def save(self, user):
        """Insert user order data to the database."""
        query = """ INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"""
        new_record = (user.name, user.email, user._password)
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(query, new_record)
                    self.db.commit()
                    return user

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error inserting new user", error

    def fetch_by_id(self, user_id):
        """Fetch one user by their id."""
        query = """ SELECT * FROM users WHERE user_id = % s"""
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    user_id, *fields = cursor.fetchone()
                    user = UserModel(*fields, user_id)
                    return user

        except (Exception, psycopg2.DatabaseError) as error:
            return "Error fetching user", error