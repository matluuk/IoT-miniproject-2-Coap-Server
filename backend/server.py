import argparse
import datetime
import logging
import os
import sys
import ipaddress
import database
import json

import asyncio

import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap

from pathlib import Path

DEFAULT_IP_ADRESS = "10.166.0.2"
DEFAULT_PORT = 5683

class TemperatureResource(resource.Resource):
    """Resource to put Temperature data to the server. It supports only PUT methods."""

    def __init__(self):
        super().__init__()
        self.set_content(0)
        self.logger = logging.getLogger('TemperatureResource')

    def set_content(self, content):
        self.content = content

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.logger.info('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        temperature = request.payload.decode()
        write_temperature_to_file(temperature)
        
        return aiocoap.Message(code=aiocoap.CHANGED)
    
class DataResource(resource.Resource):
    """Resource to post data to the server and store it for client. It supports POST and GET methods."""

    def __init__(self):
        super().__init__()
        self.set_content(0)
        self.db = database.Database()
        self.logger = logging.getLogger('DataResource')

    def set_content(self, content):
        self.content = content

    async def render_post(self, request):
        try:
            data_json = request.payload.decode()
            data = json.loads(data_json)
            
            # Check for required fields
            required_fields = ["time", "latitude", "longitude", "altitude", "accuracy"]
            if not all(field in data for field in required_fields):
                return aiocoap.Message(code=aiocoap.BAD_REQUEST)

            self.db.write_data(data)
            return aiocoap.Message(code=aiocoap.CHANGED, token=request.token)
        except json.JSONDecodeError:
            # Return a "4.00 Bad Request" response if the payload is not valid JSON
            return aiocoap.Message(code=aiocoap.BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred in render_post: {e}")
            return aiocoap.Message(code=aiocoap.INTERNAL_SERVER_ERROR)

    async def render_get(self, request):
        try:
            msg = f"GET token: {request.token} payload: {request.payload}"
            print(msg)
            self.logger.info(msg)
            self.set_content(request.payload)
            request_msg = request.payload.decode()

            # Read data from database
            data = {
                "data": self.db.read_all_data()
            }

            data_json = json.dumps(data)

            # Send the file data as payload 
            return aiocoap.Message(payload=str(data_json).encode(), code=aiocoap.CONTENT, token=request.token)
        except Exception as e:
            print(f"An error occurred in render_get: {e}")
            return aiocoap.Message(code=aiocoap.INTERNAL_SERVER_ERROR)

class DeviceConfigResource(resource.Resource):
    """Resource to manage device configurations. It supports GET and PUT methods."""

    def __init__(self):
        super().__init__()
        self.db = database.Database()
        self.logger = logging.getLogger('DeviceConfigResource')

    async def render_get(self, request):
        msg = f"GET token: {request.token} payload: {request.payload}"
        print(msg)
        self.logger.info(msg)
        try:
            device_id = request.payload.decode()
            self.logger.debug(f"Received device_id: {device_id}")
            device_config = self.db.read_device_config(device_id)
            return aiocoap.Message(payload=json.dumps(device_config).encode(), content_format=ContentFormat.JSON, code=aiocoap.CONTENT)
        except Exception as e:
            self.logger.error(f"Failed to get device config: {e}")
            return aiocoap.Message(code=aiocoap.INTERNAL_SERVER_ERROR, token=request.token)

    async def render_put(self, request):
        msg = f"PUT token: {request.token} payload: {request.payload}"
        print(msg)
        self.logger.info(msg)
        try:
            device_config = json.loads(request.payload.decode())
            self.logger.debug(f"Received device config: {device_config}")
            self.db.set_device_config(device_config) 
            return aiocoap.Message(code=aiocoap.CHANGED, token=request.token)
        except Exception as e:
            self.logger.error(f"Failed to update device config: {e}")
            return aiocoap.Message(code=aiocoap.INTERNAL_SERVER_ERROR, token=request.token)

def set_logger():
    logs_dir = os.path.join(Path(__file__).resolve().parent, "logs")

    if not os.path.exists("logs"):
        os.mkdir(logs_dir)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
    logfile = logs_dir + f"/CoAp_server_{current_time}.log"
    print(logfile)

    logging.basicConfig(filename=logfile,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.debug("Logger set up")

def write_temperature_to_file(temperature):
    data_dir = os.path.join(Path(__file__).resolve().parent, "data")

    if not os.path.exists("data"):
        os.mkdir(data_dir)
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    temperatureFile = data_dir + f"/temperature_{current_time}.txt"
    f = open(temperatureFile, "a")

    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
    f.write(f"{current_time},{temperature}\n")
    f.close()
  
async def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Start the server.')
    parser.add_argument('--ip', help='The IP address of the server.')
    parser.add_argument('--port', type=int, help='The port number of the server.')
    parser.add_argument('--output', '-o', help='The file to write the output to. If not specified, the output is written to stdout.')

    # Parse the command-line arguments
    args = parser.parse_args()

    ip_address = DEFAULT_IP_ADRESS
    port = DEFAULT_PORT

    # Redirect the output to a file if specified
    if args.output:
        sys.stdout = open(args.output, 'w')
        sys.stderr = open(args.output, 'w')
    if args.ip:
        ip_address = args.ip
    if args.port:
        port = args.port

    set_logger()
    logger = logging.getLogger("main")

    # Create an instance of the Database class
    db = database.Database()
    db.initialize_db()

    # Resource tree creationS
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['temperature'], TemperatureResource())
    root.add_resource(['data'], DataResource())
    root.add_resource(['device_config'], DeviceConfigResource())

    logger.info(f"server ip={ip_address}, port={port}")
    
    await aiocoap.Context.create_server_context(root, bind=(ip_address, port))

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())