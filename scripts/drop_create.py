import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration
DB_NAME = 'hockey'
DB_USER = 'postgres'
DB_PASSWORD = 'database'
DB_HOST = 'localhost'
DB_PORT = '5432'

def create_hockey_database():
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create the 'hockey' database
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        cur.close()

        print(f"Database '{DB_NAME}' created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating database: {e}")

    finally:
        conn.close()

def drop_hockey_database():
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Drop the 'hockey' database
        cur = conn.cursor()
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(DB_NAME)))
        cur.close()

        print(f"Database '{DB_NAME}' dropped successfully.")

    except psycopg2.Error as e:
        print(f"Error dropping database: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    # Uncomment one of the following lines to create or drop the database
    drop_hockey_database()
    create_hockey_database()
