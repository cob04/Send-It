import psycopg2

url = "dbname='sendit' host='localhost' port='5432' user='eric' password='hardpassword'"


def connection(url):
    conn = psycopg2.connect(url)
    return conn


def init_db():
    return connection(url)


def create_tables():
    try:
        conn = connection(url)
        cursor = conn.cursor()
        queries = create_table_queries()

        for query in queries:
            cursor.execute(query)
        conn.commit()
        print("Tables created successfully in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL tables", error)

    finally:
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def destroy_tables(*tables):
    try:
        conn = connection(url)
        cursor = conn.cursor()
        drop_query = "DROP TABLE IF EXISTS %s CASCADE"
        for table in tables:
            query = drop_query % table
            cursor.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return "Error while destroying PostgresSQL tables", error

    finally:
        if(conn):
            cursor.close()
            conn.close()


def create_table_queries():
    parcels = """CREATE TABLE IF NOT EXISTS parcels (
        parcel_id serial PRIMARY KEY NOT NULL,
        user_id int NOT NULL,
        sender character varying(50) NOT NULL,
        recipient character varying(50) NOT NULL,
        pickup character varying(50) NOT NULL,
        destination character varying(50) NOT NULL,
        weight numeric NOT NULL,
        status character varying(50))"""

    users = """CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY NOT NULL,
        name character varying(50) NOT NULL,
        email character varying(50) NOT NULL,
        password character varying(500) NOT NULL)"""

    queries = [parcels, users]
    return queries
