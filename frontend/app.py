import argparse
import json
import sys

from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from aiocoap import Context, Message, GET, PUT
import asyncio

DEFAULT_IP_ADRESS = "10.166.0.2"
DEFAULT_PORT = 5000

DEFAULT_SERVER_IP_ADRESS = "10.166.0.2"
DEFAULT_SERVER_PORT = 5683

global server_ip_address, server_port, ip_address, port

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def parse_args():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Start the server.')
    parser.add_argument('--ip', help='The IP address of the API server.')
    parser.add_argument('--port', type=int, help='The port number of the API server.')
    parser.add_argument('--server_ip', help='The IP address of the CoAp server.')
    parser.add_argument('--server_port', type=int, help='The port number of the CoAp server.')
    parser.add_argument('--output', '-o', help='The file to write the output to. If not specified, the output is written to stdout.')

    # Parse the command-line arguments
    args = parser.parse_args()

    global server_ip_address, server_port, ip_address, port

    ip_address = DEFAULT_IP_ADRESS
    port = DEFAULT_PORT

    server_ip_address = DEFAULT_SERVER_IP_ADRESS
    server_port = DEFAULT_SERVER_PORT

    # Redirect the output to a file if specified
    if args.output:
        print(f"Redirecting output to file {args.output}")
        sys.stdout = open(args.output, 'w')
        sys.stderr = open(args.output, 'w')
    if args.server_ip:
        server_ip_address = args.server_ip
    if args.server_port:
        server_port = args.server_port
    if args.ip:
        ip_address = args.ip
    if args.port:
        port = args.port

@app.route('/api/data', methods=['GET'])
def get_data():
    async def main():
        # Replace with your CoAP server's address
        coap_server_url = f'coap://{server_ip_address}:{server_port}/data'
        
        # Create a new CoAP client
        protocol = await Context.create_client_context()

        # Create a new GET coap_request
        coap_request = Message(code=GET, uri=coap_server_url)

        # Send the coap_request
        response = await protocol.request(coap_request).response

        # Parse the response as JSON
        data = json.loads(response.payload.decode())

        print(data)

        # Return the data as JSON
        return jsonify(data)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(main())

@app.route('/api/config', methods=['GET', 'PUT'])
def config():
    async def handle_get():
        # Replace with your CoAP server's address
        coap_server_url = f'coap://{server_ip_address}:{server_port}/config'
        
        # Create a new CoAP client
        protocol = await Context.create_client_context()

        # Create a new GET coap_request
        coap_request = Message(code=GET, uri=coap_server_url)

        # Send the coap_request
        response = await protocol.request(coap_request).response

        # Parse the response as JSON
        data = json.loads(response.payload.decode())

        print(data)

        # Return the data as JSON
        return jsonify(data)
    
    async def handle_put():
        # Replace with your CoAP server's address
        coap_server_url = f'coap://{server_ip_address}:{server_port}/config'
        
        # Create a new CoAP client
        protocol = await Context.create_client_context()

        # Get the JSON data from the request
        data = request.get_json()

        # Create a new PUT request
        coap_request = Message(code=PUT, uri=coap_server_url, payload=json.dumps(data))

        # Send the request
        response = await protocol.request(request).response

        # Return the response status code
        return str(response.code)


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if request.method == 'GET':
        return loop.run_until_complete(handle_get())
    elif request.method == 'PUT':
        return loop.run_until_complete(handle_put())

if __name__ == '__main__':
    parse_args()
    app.run(debug=False, host=ip_address, port=port)
