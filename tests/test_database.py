import unittest
import logging
import os
import tests.utils as utils
from sqlite3 import Error
from database import Database

DATABASE_FILE = 'test.db'

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utils.set_logger()
        cls.logger = logging.getLogger('TestDatabase')
    
    def setUp(self):
        pass

    def tearDown(self):
        # Close the database connection
        self.db.conn.close()

        # Remove the test database file
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)

    def test_create_database(self): 
        self.logger.info("Testing create_connection")

        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        self.assertIsNotNone(self.db.conn, "Failed to create database connection")

    def test_connect_to_existing_database(self): 
        self.logger.info("Testing test_connect_to_existing_database")

        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        self.assertIsNotNone(self.db.conn, "Failed to create database connection")

        
        self.db2 = Database(db_file=DATABASE_FILE)
        self.db2.initialize_db()
        self.assertIsNotNone(self.db2.conn, "Failed to create database connection")
    
    def test_create_data_table(self):
        self.logger.info("Testing test_create_data_table")

        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        with self.assertRaises(Error):
            self.db.create_data_table()
    
    def test_create_device_configs_table(self):
        self.logger.info("Testing test_create_device_configs_table")

        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        with self.assertRaises(Error):
            self.db.create_device_configs_table()

    def test_write_data(self):
        self.logger.info("Testing test_write_data")

        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        data = {'time': 1633028200, 'latitude': 40.712776, 'longitude': -74.005974, 'altitude': 0.0, 'accuracy': 0.0}
        self.db.write_data(data)

    def test_read_empty_all_data(self):
        self.logger.info("Testing test_read_all_data")
        
        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        data = self.db.read_all_data()
        self.assertIsInstance(data, list, "read_all_data should return a list")
        self.assertEqual(len(data), 0, "read_all_data should return an empty list")
    
    def test_write_and_read_data(self):
        self.logger.info("Testing test_write_and_read_data")

        
        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        data = {'time': 1633028200, 'latitude': 40.712776, 'longitude': -74.005974, 'altitude': 0.0, 'accuracy': 0.0}
        self.db.write_data(data)
        read_data = self.db.read_all_data()
        self.assertIsInstance(read_data, list, "read_all_data should return a list")
        self.assertIn(data, read_data, "The written data is not in the read data")

    def test_update_device_config(self):
        self.logger.info("Testing test_set_device_config")

        
        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        device_config = {
            'device_id': 'test_device',
            'active_mode': True,
            'location_timeout': 300,
            'active_wait_timeout': 600,
            'passive_wait_timeout': 1200
        }
        self.db.set_device_config(device_config)

        read_config = self.db.read_device_config(device_config['device_id'])
        self.assertIsInstance(read_config, dict, "read_device_config should return a dict")
        self.assertEqual(read_config, device_config, "The read config is not the same as the written config")

        device_config['active_mode'] = False
        device_config['location_timeout'] = 600

        self.db.set_device_config(device_config)

        read_config = self.db.read_device_config(device_config['device_id'])
        self.assertIsInstance(read_config, dict, "read_device_config should return a dict")
        self.assertEqual(read_config, device_config, "The read config is not the same as the written config")

    def test_read_empty_device_config(self):
        self.logger.info("Testing test_read_empty_device_config")

        
        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        device_id = '123'
        config = self.db.read_device_config(device_id)
        self.assertIsNone(config, "read_device_config should return a None")

    def test_set_and_read_device_config(self):
        self.logger.info("Testing test_set_and_read_device_config")

        
        self.db = Database(db_file=DATABASE_FILE)
        self.db.initialize_db()
        device_config = {
            'device_id': '1234',
            'active_mode': True,
            'location_timeout': 300,
            'active_wait_timeout': 600,
            'passive_wait_timeout': 1200
        }
        self.db.set_device_config(device_config)
        read_config = self.db.read_device_config(device_config['device_id'])
        self.assertIsInstance(read_config, dict, "read_device_config should return a dict")
        self.assertEqual(read_config, device_config, "The read config is not the same as the written config")

if __name__ == '__main__':
    unittest.main()