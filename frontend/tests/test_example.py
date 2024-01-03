import unittest
import logging
import os
import tests.utils as utils

DATABASE_FILE = 'test.db'

class TestExample(unittest.TestCase):
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
        pass

if __name__ == '__main__':
    unittest.main()