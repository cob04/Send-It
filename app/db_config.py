import psycopg2
from flask import current_app

# url = "dbname='sendit' host='localhost' port='5432' user='eric' password='hardpassword'"
 
def connection():
    url = current_app.config["DATABASE_URL"]
    conn = psycopg2.connect(url)
    return conn


def init_db():
    return connection()


def create_tables():
    try:
        with connection() as conn:
            with conn.cursor() as cursor:
                queries = create_table_queries()

                for query in queries:
                    cursor.execute(query)
                    conn.commit()
                print("Tables created successfully in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL tables", error)


def destroy_tables(table):
    try:
        with connection() as conn:
            with conn.cursor() as cursor:
                drop_query = """DROP TABLE IF EXISTS %s CASCADE"""
                cursor.execute(query, (table,))

    except (Exception, psycopg2.DatabaseError) as error:
        return "Error while destroying PostgresSQL tables", error


def create_table_queries():
    parcels = """CREATE TABLE IF NOT EXISTS parcels (
        parcel_id serial PRIMARY KEY NOT NULL,
        user_id int NOT NULL,
        sender character varying(50) NOT NULL,
        recipient character varying(50) NOT NULL,
        pickup character varying(50) NOT NULL,
        destination character varying(50) NOT NULL,
        weight numeric NOT NULL,
        status character varying(50),
        present_location character varying(50))"""

    users = """CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY NOT NULL,
        name character varying(50) NOT NULL,
        email character varying(50) UNIQUE NOT NULL,
        password character varying(500) NOT NULL,
        role character varying(20))"""

    queries = [parcels, users]
    return queries
