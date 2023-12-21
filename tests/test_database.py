import datetime
from pathlib import Path
import unittest
import logging
import os
from sqlite3 import Error
from database import Database

DATABASE_FILE = 'test.db'

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_logger()
    
    def setUp(self):
        pass

    def tearDown(self):
        # Close the database connection
        self.db.conn.close()

        # Remove the test database file
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)

    def test_create_connection(self): 
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing create_connection")
        self.assertIsNotNone(self.db.conn, "Failed to create database connection")

    def test_write_data(self):
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing test_write_data")
        data = {'time': 1633028200, 'latitude': 40.712776, 'longitude': -74.005974, 'altitude': 0.0, 'accuracy': 0.0}
        try:
            self.db.write_data(data)
        except Error:
            self.fail("write_data raised Error unexpectedly!")

    def test_read_all_data(self):
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing test_read_all_data")
        try:
            data = self.db.read_all_data()
            self.assertIsInstance(data, list, "read_all_data should return a list")
        except Error:
            self.fail("read_all_data raised Error unexpectedly!")
    
    def test_write_and_read_data(self):
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing test_write_and_read_data")
        data = {'time': 1633028200, 'latitude': 40.712776, 'longitude': -74.005974, 'altitude': 0.0, 'accuracy': 0.0}
        try:
            self.db.write_data(data)
            read_data = self.db.read_all_data()
            self.assertIsInstance(read_data, list, "read_all_data should return a list")
            self.assertIn(data, read_data, "The written data is not in the read data")
        except Error:
            self.fail("write_data or read_all_data raised Error unexpectedly!")
    
    def test_set_device_config(self):
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing test_set_device_config")
        device_config = {
            'device_id': 'test_device',
            'active_mode': True,
            'location_timeout': 300,
            'active_wait_timeout': 600,
            'passive_wait_timeout': 1200
        }
        try:
            self.db.set_device_config(device_config)
        except Error:
            self.fail("set_device_config raised Error unexpectedly!")

    def test_read_device_config(self):
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing test_read_device_config")
        device_id = 'test_device'
        try:
            config = self.db.read_device_config(device_id)
            self.assertIsInstance(config, dict, "read_device_config should return a dict")
            self.assertEqual(config['device_id'], device_id, "The read config is not the same as the written config")
        except Error:
            self.fail("read_device_config raised Error unexpectedly!")

    def test_set_and_read_device_config(self):
        self.db = Database(db_file=DATABASE_FILE)
        self.logger.info("Testing test_set_and_read_device_config")
        device_config = {
            'device_id': 'test_device',
            'active_mode': True,
            'location_timeout': 300,
            'active_wait_timeout': 600,
            'passive_wait_timeout': 1200
        }
        try:
            self.db.set_device_config(device_config)
            read_config = self.db.read_device_config(device_config['device_id'])
            self.assertIsInstance(read_config, dict, "read_device_config should return a dict")
            self.assertEqual(read_config, device_config, "The read config is not the same as the written config")
        except Error:
            self.fail("set_device_config or read_device_config raised Error unexpectedly!")
    
    @classmethod
    def set_logger(cls):
        logs_dir = os.path.join(Path(__file__).resolve().parent, "test_logs")

        if not os.path.exists(logs_dir):
            os.mkdir(logs_dir)

        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
        logfile = logs_dir + f"/TestDatabase_{current_time}.log"

        # Get the root logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Create a file handler
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # Create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        logging.debug("Logger set up")
        cls.logger = logging.getLogger('TestDatabase')

if __name__ == '__main__':
    unittest.main()