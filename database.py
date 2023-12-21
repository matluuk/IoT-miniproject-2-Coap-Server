import sqlite3
from sqlite3 import Error

import logging
logger = logging.getLogger('database')

# This class is used to create a SQLite database and write data to it

class Database():
    def __init__(self):
        self.conn = self.__create_connection()

    def __create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('sqlite_database.db')  # Creates a SQLite database in the current directory
            logger.info(sqlite3.version)
        except Error as e:
            logger.error(e)
        return conn

    def intialize_db(self):
        self.create_device_configs_table()
        self.create_data_table()

    def create_data_table(self):
        try:
            c = self.conn.cursor()
            c.execute("CREATE TABLE data " +
                    "(time INTEGER, " +
                    "latitude DOUBLE, " +
                    "longitude DOUBLE, " +
                    "altitude REAL, " +
                    "accuracy REAL)")
        except Error as e:
            logger.error(e)
    
    def create_device_configs_table(self):
        try:
            c = self.conn.cursor()
            c.execute("CREATE TABLE device_configs " +
                      "(device_id VARCHAR(50) NOT NULL, " +
                      "active_mode INTEGER, " +
                      "location_timeout INTEGER, " +
                      "active_wait_timeout INTEGER, " +
                      "passive_wait_timeout INTEGER), " +
                      "PRIMARY KEY(device_id)")
        except Error as e:
            logger.error(e)

    def write_data(self, data):
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO data (time, latitude, longitude, altitude, accuracy) 
                    VALUES (:time, :latitude, :longitude, :altitude, :accuracy)
                """, data)
        except Error as e:
            logger.error(e)

    def read_all_data(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM data")
            columns = [column[0] for column in c.description]
            data = [dict(zip(columns, row)) for row in c.fetchall()]
            return data
        except Error as e:
            logger.error(e)
    
    def update_device_config(self, device_config):
        try:
            c = self.conn.cursor()
            c.execute("""
                UPDATE device_configs 
                SET active_mode = ?, 
                    location_timeout = ?, 
                    active_wait_timeout = ?, 
                    passive_wait_timeout = ? 
                WHERE device_id = ?
            """, (device_config["active_mode"], device_config["location_timeout"], device_config["active_wait_timeout"], device_config["passive_wait_timeout"], device_config["device_id"]))
            self.conn.commit()
        except Error as e: 
            logger.error(e)

    def read_device_config(self, device_id):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM device_configs WHERE device_id = ?", (device_id,))
            columns = [column[0] for column in c.description]
            data = c.fetchone()
            if data is None:
                return None
            return dict(zip(columns, data))
        except Error as e:
            logger.error(e)