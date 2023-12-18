import sqlite3
from sqlite3 import Error

class Database():
    def __init__(self):
        self.conn = self.__create_connection()

    def __create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('sqlite_database.db')  # Creates a SQLite database in the current directory
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE temperature
                        (date text, temp real)''')
        except Error as e:
            print(e)

    def write_data_to_db(self, date, temp):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO temperature VALUES (?,?)", (date, temp))
            self.conn.commit()
        except Error as e:
            print(e)

    def read_data_from_db(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM temperature")
            return c.fetchall()
        except Error as e:
            print(e)