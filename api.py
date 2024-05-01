from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import controllers
from getpass import getpass
from mysql.connector import connect, Error


db_user = input("Enter username: ")
db_password = getpass("Enter password: ")

try:
    with connect(
        host="127.0.0.1",
        user=db_user,
        password=db_password,
        database="demo3db",
    ) as connection:
        with connection.cursor() as cursor:
            show_db_query = "SHOW DATABASES"
            print('Database Connected')
except Error as e:
    print(e)


class APIServer(BaseHTTPRequestHandler):
  
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        path = self.path
        response = None

        # to authenticate a user
        if path == '/authenticate':
            username = data.get('username')
            password = data.get('password')
            user = controllers.authenticate_user(username, password)
            if user:
                response = {'message': 'User authenticated successfully'}
            else:
                self.send_response(401)
                self.end_headers()
                response = {'error': 'Invalid username or password'}

        # to register a user
        elif path == '/register':
            username = data.get('username')
            password = data.get('password')
            if controllers.register_user(username, password):
                response = {'message': 'User registered successfully'}
            else:
                self.send_response(500)
                self.end_headers()
                response = {'error': 'Failed to register user'}

        if response:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))


def run_server():
    host = 'localhost'
    port = 8080
    server_address = (host, port)
    httpd = HTTPServer(server_address, APIServer)
    print(f'Server running on {host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
