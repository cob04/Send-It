import psycopg2

from werkzeug.security import  generate_password_hash, check_password_hash

from app.db_config import init_db

from ..exceptions import (IncorrectPasswordError, UserNotFoundError,
                          ApplicationError, EmailNotUniqueError)

ADMIN = "Administrator"
NORMAL = "Normal"


class UserModel:
    """Object to store user data.
    This makes it easy to manipulate.
    """
    def __init__(self, name, email, password, user_id=None, role=None):

        self.id = user_id
        self.name = name
        self.email = email
        self._password = password 
        if role:
            self.role = role
        else:
            self.role = NORMAL

    def __repr__(self):
        return "User(%s, %s, %s)" % (self.name, self.email, self.role)

    def __eq__(self, other):
        """Compare users by their attributes."""
        return self.__dict__ == other.__dict__

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
    """Object to abstract away the database.
    Handles inserting and retriving data from the database.
    """
    def __init__(self):
        self.db = init_db()

    def save(self, user):
        """Insert user order data to the database."""
        query = """ INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"""
        password_hash = generate_password_hash(user._password)
        new_record = (user.name, user.email, password_hash, user.role)
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(query, new_record)
                    self.db.commit()
                    return user

        except psycopg2.IntegrityError:
            raise EmailNotUniqueError

        except psycopg2.Error as e:
            print("<<<<< ", e)
            raise ApplicationError

    def fetch_by_id(self, user_id):
        """Fetch one user by their id."""
        query = """ SELECT * FROM users WHERE user_id = %s"""
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    result = cursor.fetchone()
                    if result:
                        user_id, *fields, role = result
                        user = UserModel(*fields, user_id=user_id, role=role)
                        return user
                    else:
                        raise UserNotFoundError

        except psycopg2.IntegrityError:
            raise EmailNotUniqueError

        except psycopg2.Error:
            raise ApplicationError

    def authenticate(self, email, password):
        """Verify email and password."""
        query = """SELECT * FROM users WHERE email = '{}'""".format(email)
        try:
            with self.db:
                with self.db.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result:
                        user_id, *fields, role = result
                        user = UserModel(*fields, user_id=user_id, role=role)
                        if check_password_hash(user._password, password):
                            return user
                        else:
                            raise IncorrectPasswordError
                    else:
                        raise UserNotFoundError

        except psycopg2.Error:
            raise ApplicationError
