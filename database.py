import sqlite3
from sqlite3 import Error
import logging

# This class is used to create a SQLite database and write data to it

class Database():
    def __init__(self):
        self.logger = logging.getLogger('Database')
        self.conn = self.__create_connection()

    def __create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('sqlite_database.db')  # Creates a SQLite database in the current directory
            self.logger.info(f"Connected to database with sqlite version {sqlite3.version}")
        except Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
        return conn

    def initialize_db(self):
        c = self.conn.cursor()

        # Check if the 'device_configs' table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='device_configs'")
        if not c.fetchone():
            self.logger.info("Creating 'device_configs' table")
            self.create_device_configs_table()

        # Check if the 'data' table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
        if not c.fetchone():
            self.logger.info("Creating 'data' table")
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
            self.logger.error(f"Failed to create 'data' table: {e}")
            raise
    
    def create_device_configs_table(self):
        try:
            c = self.conn.cursor()
            c.execute("CREATE TABLE device_configs " +
                      "(device_id VARCHAR(50) NOT NULL, " +
                      "active_mode INTEGER, " +
                      "location_timeout INTEGER, " +
                      "active_wait_timeout INTEGER, " +
                      "passive_wait_timeout INTEGER, " +
                      "PRIMARY KEY(device_id))")
        except Error as e:
            self.logger.error(f"Failed to create 'device_config' table: {e}")
            raise

    def write_data(self, data):
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO data (time, latitude, longitude, altitude, accuracy) 
                    VALUES (:time, :latitude, :longitude, :altitude, :accuracy)
                """, data)
            self.logger.info("Write data successfully to 'data' table")
        except Error as e:
            self.logger.error(f"Failed to write data to 'data' table: {e}")
            raise

    def read_all_data(self):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM data")
            columns = [column[0] for column in c.description]
            data = [dict(zip(columns, row)) for row in c.fetchall()]
            self.logger.info("Read all data successfully")
            return data
        except Error as e:
            self.logger.error(f"Failed to read all data: {e}")
            raise

    def set_device_config(self, device_config):
        device_id = device_config['device_id']
        existing_config = self.check_if_device_config_exists(device_id)
        if existing_config is not None:
            self.logger.info(f"Updating device config for device_id: {device_id}")
            self.update_device_config(device_config)
        else:
            self.logger.info(f"Adding new device config for device_id: {device_id}")
            self.add_device_config(device_config)

    
    def add_device_config(self, device_config):
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO device_configs (device_id, active_mode, location_timeout, active_wait_timeout, passive_wait_timeout) 
                    VALUES (:device_id, :active_mode, :location_timeout, :active_wait_timeout, :passive_wait_timeout)
                """, device_config)
            self.logger.info(f"Added new device config for device_id: {device_config['device_id']}")
        except Error as e:
            self.logger.error(f"Failed to add device config: {e}")
            raise


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
            self.logger.info(f"Updated device config for device_id: {device_config['device_id']}")
        except Error as e: 
            self.logger.error(f"Failed to update device config: {e}")
            raise

    def read_device_config(self, device_id):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM device_configs WHERE device_id = ?", (device_id,))
            columns = [column[0] for column in c.description]
            data = c.fetchone()
            if data is None:
                self.logger.info(f"No device config found for device_id: {device_id}")
                return None
            self.logger.info(f"Read device config for device_id: {device_id}")
            return dict(zip(columns, data))
        except Error as e:
            self.logger.error(f"Failed to read device config for device_id {device_id}: {e}")
            raise
    
    def check_if_device_config_exists(self, device_id):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM device_configs WHERE device_id = ?", (device_id,))
            data = c.fetchone()
            if data is None:
                self.logger.info(f"No device config found for device_id: {device_id}")
                return False
            self.logger.info(f"Read device config for device_id: {device_id}")
            return True
        except Error as e:
            self.logger.error(f"Failed to read device config for device_id {device_id}: {e}")
            raise