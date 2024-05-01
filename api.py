from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from controllers import *
from schema import *
from getpass import getpass
from mysql.connector import connect, Error

controllers = get_controllers()

filelistcontroller_instance = controllers['filelistcontroller']()
datasetscontroller_instance = controllers['datasetscontroller']()
recordingcontroller_instance = controllers['recordingcontroller']()

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
            user = authenticate_user(username, password)
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
            if register_user(username, password):
                response = {'message': 'User registered successfully'}
            else:
                self.send_response(500)
                self.end_headers()
                response = {'error': 'Failed to register user'}

        # to create a group
        elif path == '/create_group':
            group_name = data.get('group_name')
            usernames = data.get('usernames', [])
            existing_usernames = [
                username for username in usernames if get_user_by_username(username)]
            if len(existing_usernames) == len(usernames):
                group = create_group(
                    group_name, existing_usernames)
                if group:
                    response = {'message': 'Group created successfully',
                                'group': {'id': group.id, 'name': group.name}}
                else:
                    self.send_response(500)
                    self.end_headers()
                    response = {'error': 'Failed to create group'}
            else:
                self.send_response(400)
                self.end_headers()
                response = {'error': 'Invalid usernames provided'}

        # to create a dataset
        elif path == '/dataset/create':
            ent_dataset = EntDataset(**data)
            datasetscontroller_instance.create_dataset(ent_dataset)
            
            self.send_response(201)
            self.end_headers()
            self.wfile.write(bytes("Dataset created successfully", "utf-8"))

        elif self.path == '/recording':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            recording_data = data.get('recording')
            user_data = data.get('user')

            user = EntUser(**user_data)
            user_id = UserController.create_user(user)

            recording = EntRecording(**recording_data, user_credentials=user_id)
            recordingcontroller_instance.create_recording(recording)
            
            self.send_response(201)
            self.end_headers()
            self.wfile.write(bytes("Recording created successfully", "utf-8"))

        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid action')

        if response:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

     # Retrieve all datasets or a specific dataset
    def do_GET(self):
        if self.path == '/dataset':
            datasets = datasetscontroller_instance.get_all_datasets()
            datasets_json = [ent_dataset.__dict__ for ent_dataset in datasets]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(datasets_json), "utf-8"))
        else:
            query_components = parse_qs(self.path[2:])
            if 'id' in query_components:
                dataset_id = query_components['id'][0]
                dataset = datasetscontroller_instance.get_dataset(dataset_id)
                if dataset:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(dataset.__dict__), "utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(bytes("Dataset not found", "utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes("Missing dataset ID in query parameters", "utf-8"))

    # Update a dataset
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        if self.path == '/dataset/update':
            ent_dataset = EntDataset(**data)
            datasetscontroller_instance.update_dataset(ent_dataset)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Dataset updated successfully", "utf-8"))

        elif self.path == '/recording/update':
            ent_recording = EntRecording(**data)
            update_recording(ent_recording)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Recording updated successfully", "utf-8"))
        elif self.path.startswith('/filelist'):
            filelist = EntFilelist(**data)
            filelistcontroller_instance.update_filelist(filelist)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("File list updated successfully", "utf-8"))
    # Delete a dataset
    def do_DELETE(self):
        if self.path == '/dataset/delete':
            query_components = parse_qs(self.path[2:])
            if 'id' in query_components:
                dataset_id = query_components['id'][0]
                datasetscontroller_instance.delete_dataset(dataset_id)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes("Dataset deleted successfully", "utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(
                    bytes("Missing dataset ID in query parameters", "utf-8"))


def run_server():
    host = 'localhost'
    port = 8080
    server_address = (host, port)
    httpd = HTTPServer(server_address, APIServer)
    print(f'Server running on {host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
