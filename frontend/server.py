import argparse
import subprocess
import http.server
import socketserver
import sys

DEFAULT_PORT = 8000
DEFAULT_IP_ADRESS = "10.166.0.2" 

def parse_args():
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
    return ip_address, port

def start_http_server(ip_address=DEFAULT_IP_ADRESS, port=DEFAULT_PORT):
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((ip_address, port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()

def start_app():
    subprocess.Popen(["python", "app.py"])

if __name__ == '__main__':
    ip_address, port = parse_args()
    start_app()
    start_http_server(ip_address=ip_address, port=port)