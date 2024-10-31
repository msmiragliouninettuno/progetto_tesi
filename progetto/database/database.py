import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_SERVER = os.getenv('SQL_SERVER')

class db:
    connection = None
    connected = False

    @staticmethod
    def connect():
        db.closeConnection()
        
        DATABASE = "studenti"
        connectionString = {
            'host': SQL_SERVER,
            'user': SQL_USERNAME,
            'password': SQL_PASSWORD,
            'database': DATABASE,
            'charset': 'utf8mb4',  # Forza l'uso del set di caratteri utf8mb4
            'collation': 'utf8mb4_general_ci'  # Collation compatibile
        }

        db.connection = mysql.connector.connect(**connectionString)
        db.connected = True

        return db.connection

    @staticmethod
    def closeConnection():
        if db.connected:
            db.connection.close()
            db.connected = False

    def __del__(self):
        db.closeConnection()
