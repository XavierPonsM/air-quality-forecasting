import os
import psycopg2
from psycopg2 import Error
 
def data():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(os.environ["DATABASE_URL"])
 
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        #cursor.execute("select * from public.ranking")
        cursor.execute("""
                        SELECT nom_estacio, "data", contaminant, unitats, latitud, longitud, no2
                        FROM definitiu.no2_csv

                        """)
       
        # Fetch result
        record = cursor.fetchall()
        return record
 
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
