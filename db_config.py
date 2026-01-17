#Configuring the database connection.

import mysql.connector

def get_connection():
    return mysql.connector.connect(
    host="localhost",
    user="saurav",
    password="123321",
    database="library_db"
    )
 
