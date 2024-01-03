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
        data_json = '{"time": "2021-05-01 13:00:00", "latitude": 12.345, "longitude": 67.890, "altitude": 123.456, "accuracy": 12.345}'
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