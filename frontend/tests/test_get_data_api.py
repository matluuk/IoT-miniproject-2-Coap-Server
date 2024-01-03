import unittest
from flask_testing import TestCase
from app import app
import json

class TestGetDataApi(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_data(self):
        response = self.client.get('/api/data')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())
        self.assertIn('latitude', data)
        self.assertIn('longitude', data)
        self.assertIn('altitude', data)
        self.assertIn('accuracy', data)
        self.assertIn('time', data)

if __name__ == '__main__':
    unittest.main()