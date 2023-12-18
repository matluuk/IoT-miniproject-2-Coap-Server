import datetime
import logging
import os
import sys
import ipaddress

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
        temperature = request.payload # .decode()
        write_temperature_to_file(temperature)
        
        return aiocoap.Message(code=aiocoap.CHANGED)

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
    set_logger()
    logger = logging.getLogger("main")

    # Resource tree creation
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['temperature'], TemperatureResource())

    ip_address = DEFAULT_IP_ADRESS
    port = DEFAULT_PORT

    logger.debug("parse command line arguments!")
    for arg in sys.argv[1:]:
        if "ip=" in arg:
            try:
                ip_address = arg[len("ip="):]
                ipaddress.ip_address(ip_address)
                logger.info(f"server ip={ip_address}")
            except ValueError:
                print('ip address is invalid: %s' % ip_address)
                return
        elif "port=" in arg:
            port = int(arg[len("port="):])
            logger.info(f"server port={arg}")
        else:
            print('Usage : %s  ip=<ip_address> port=<port>' % sys.argv[0])
    
    await aiocoap.Context.create_server_context(root, bind=(ip_address, port))

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
