import asyncio
import json
import subprocess
import multiprocessing
import time
import unittest
import logging
from unittest.mock import patch
from aiocoap import Context, Message, GET, POST, PUT, CHANGED, CONTENT
import aiocoap

import tests.utils as utils

from server import main as server_main

VENV_PATH = 'venv/bin/python'

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utils.set_logger()
        cls.logger = logging.getLogger('TestDatabase')
        # Start the server in a separate process
        # cls.server_process = multiprocessing.Process(target=server_main, args=('--output', 'server_output.out', '--ip', '127.0.0.1',))

        # Allow some time for the server to start
        time.sleep(1)

    async def setup_context(self):
        self.context = await Context.create_client_context()

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.setup_context())

    @classmethod
    def tearDownClass(cls):
        # Terminate the server process when the tests are done
        # cls.server_process.terminate()
        # cls.server_process.wait()
        pass

    def test_temperature_resource_put(self):
        # Arrange
        request = Message(code=PUT, payload=b'test', uri="coap://localhost/temperature")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        self.assertEqual(response.code, CHANGED)

    def test_data_resource(self):
        data_json = '{"time": "2021-05-01 13:00:00", "latitude": 30.345, "longitude": 80.890, "altitude": 123.456, "accuracy": 12.345}'
        data = json.loads(data_json)
        payload = data_json.encode()
        # Arrange
        request = Message(code=POST, payload=payload, uri="coap://localhost/data")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        self.assertEqual(response.code, CHANGED)
        # Arrange
        request = Message(code=GET, uri="coap://localhost/data")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        self.assertEqual(response.code, CONTENT)

        response_json = response.payload.decode()
        self.logger.debug(f'response_json: {response_json}')
        response_data = json.loads(response_json)
        self.logger.debug(f'response_data: {response_data["data"]}')
        self.assertEqual(response_data["data"][-1], data)

    def test_data_resource_non_json_payload(self):
        payload = b"This is a non-JSON payload"
        # Arrange
        request = Message(code=POST, payload=payload, uri="coap://localhost/data")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        # Expecting a 4.00 Bad Request response because the payload is not JSON
        self.assertEqual(response.code, aiocoap.BAD_REQUEST)

    def test_data_resource_incomplete_json_payload(self):
        data_json = '{"time": "2021-05-01 13:00:00", "latitude": 30.345, "longitude": 80.890}'
        payload = data_json.encode()
        # Arrange
        request = Message(code=POST, payload=payload, uri="coap://localhost/data")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        # Expecting a 4.00 Bad Request response because the payload is missing some fields
        self.assertEqual(response.code, aiocoap.BAD_REQUEST)
    
    def test_multiple_data_resource(self):
        locations = [
            {"time": "2021-05-01 13:00:00", "latitude": 12.345, "longitude": 67.890, "altitude": 123.456, "accuracy": 10.345},
            {"time": "2021-05-01 13:01:00", "latitude": 13.345, "longitude": 68.890, "altitude": 124.456, "accuracy": 20.345},
            {"time": "2021-05-01 13:02:00", "latitude": 14.345, "longitude": 69.890, "altitude": 125.456, "accuracy": 30.345},
            {"time": "2021-05-01 13:03:00", "latitude": 15.345, "longitude": 70.890, "altitude": 126.456, "accuracy": 40.345},
            {"time": "2021-05-01 13:04:00", "latitude": 16.345, "longitude": 71.890, "altitude": 127.456, "accuracy": 50.345},
            {"time": "2021-05-01 13:05:00", "latitude": 17.345, "longitude": 72.890, "altitude": 128.456, "accuracy": 60.345},
            {"time": "2021-05-01 13:06:00", "latitude": 18.345, "longitude": 73.890, "altitude": 129.456, "accuracy": 70.345},
            {"time": "2021-05-01 13:07:00", "latitude": 19.345, "longitude": 74.890, "altitude": 130.456, "accuracy": 80.345},
            {"time": "2021-05-01 13:08:00", "latitude": 20.345, "longitude": 75.890, "altitude": 131.456, "accuracy": 90.345},
            {"time": "2021-05-01 13:09:00", "latitude": 21.345, "longitude": 76.890, "altitude": 132.456, "accuracy": 100.345}
        ]

        for location in locations:
            data_json = json.dumps(location)
            payload = data_json.encode()

            # Arrange
            request = Message(code=POST, payload=payload, uri="coap://localhost/data")

            # Act
            response = self.loop.run_until_complete(self.context.request(request).response)

            # Assert
            self.assertEqual(response.code, CHANGED)

        # Arrange
        request = Message(code=GET, uri="coap://localhost/data")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        self.assertEqual(response.code, CONTENT)

        response_json = response.payload.decode()
        response_data = json.loads(response_json)

        # Assert that the last 10 data points are the locations
        for i, location in enumerate(locations):
            self.assertEqual(response_data["data"][-10 + i], location)
    
    def test_device_config_resource(self):
        device_config_json = '{"device_id": "test_device_id", "active_mode": true, "location_timeout": 10, "active_wait_timeout": 10, "passive_wait_timeout": 10}'
        device_config = json.loads(device_config_json)
        payload = device_config_json.encode()
        # Arrange
        request = Message(code=PUT, payload=payload, uri="coap://localhost/device_config")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        self.assertEqual(response.code, CHANGED)

        payload = device_config["device_id"].encode()
        # Arrange
        request = Message(code=GET, payload=payload, uri="coap://localhost/device_config")

        # Act
        response = self.loop.run_until_complete(self.context.request(request).response)

        # Assert
        self.assertEqual(response.code, CONTENT)

        response_json = response.payload.decode()
        self.logger.debug(f'response_json: {response_json}')
        response_data = json.loads(response_json)
        self.logger.debug(f'response_data: {response_data}')
        self.assertEqual(response_data, device_config)

if __name__ == '__main__':
    unittest.main()