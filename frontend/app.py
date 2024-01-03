import json

from flask import Flask, jsonify
from flask_cors import CORS
from aiocoap import Context, Message, GET
import asyncio

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/api/data', methods=['GET'])
def get_data():
    async def main():
        # Replace with your CoAP server's address
        coap_server_url = 'coap://localhost/data'
        
        # Create a new CoAP client
        protocol = await Context.create_client_context()

        # Create a new GET request
        request = Message(code=GET, uri=coap_server_url)

        # Send the request
        response = await protocol.request(request).response

        # Parse the response as JSON
        data = json.loads(response.payload.decode())

        print(data)

        # Return the data as JSON
        return jsonify(data)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(main())

if __name__ == '__main__':
    app.run(debug=True)