# # You have a file with a large array of data (a million records) and a table in the database.
# #  Load the data into the table using Python (you may need to use a generator. Or not. At your discretion).

# # Path: data_insertion.py
# import psycopg2
# import random

import pdb
from datetime import datetime
import psycopg2

conn = psycopg2.connect(
                host="localhost",
                port = 5432,
                dbname="postgres"
            )

    # Crear un cursor para ejecutar consultas
cursor = conn.cursor()
            # Crear un cursor para ejecutar consultas

def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split(',')

            yield data 

def insert_data_into_table(data, table_name):
    conn = psycopg2.connect(
        host="localhost",
        port = 5432,
        database="postgres")
    cur = conn.cursor()

    for row in data:
        cur.execute(f"INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", row)
    conn.commit()
    cur.close()

fp = "/Users/macbookpro/Desktop/Programacion/my_github/user_test.csv"
table_name = 'smartstats.users'
data = read_data_from_file(fp)
insert_data_into_table(data, table_name)


    


