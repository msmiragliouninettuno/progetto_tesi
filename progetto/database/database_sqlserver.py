import pyodbc
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

        
        DATABASE = "Studenti"
        connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SQL_SERVER};DATABASE={DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD};TrustServerCertificate=yes"


        db.connection = pyodbc.connect(connectionString)
        db.connected = True

        return db.connection

    @staticmethod
    def closeConnection():
        if db.connected:
            db.connection.close()

    def __del__(self):
        db.connection.close()
