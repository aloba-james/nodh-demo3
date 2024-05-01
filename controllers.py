from schema import User, Group
import authentication
from mysql.connector import connect, Error
from api import db_password, db_user
import base64
from controllers_dir import filelist_controller, datasets_controller, recording_controller


def get_controllers():
    return {
        'filelistcontroller': filelist_controller.FileListController,
        'datasetscontroller': datasets_controller.DatasetController,
        'recordingcontroller': recording_controller.RecordingController
    }


def authenticate_user(username, password):
    return authentication.authenticate_user(username, password)

def register_user(username, password):
    return authentication.register_user(username, password)

def create_group_schema():
    try:
        with connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='demo3db'
        ) as connection:
            with connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS groups (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )"""

                # Execute the SQL command
                cursor.execute(create_table_query)
                connection.commit()

                print("Group schema created successfully.")

    except Error as e:
        print("Error creating group schema:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_user_by_username(username):
    try:
        with connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='demo3db'
        ) as connection:

            cursor = connection.cursor(dictionary=True)

            # Query the database for the user
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                user = User(**user_data)
                return user
            else:
                return None

    except Error as e:
        print("Error getting user by username:", e)
        return None


def create_group(name, usernames):
    try:
        connection = connect(
            host='localhost',
            user= db_user,
            password=db_password,
            database='demo3db'
        )

        cursor = connection.cursor()

        # Create the group in the database
        query = "INSERT INTO groups (name) VALUES (%s)"
        cursor.execute(query, (name,))
        connection.commit()

        group_id = cursor.lastrowid
        print("Group created successfully.")

        # Get user IDs for the provided usernames and add them to the group
        for username in usernames:
            user = get_user_by_username(username)
            if user:
                add_user_to_group(user.id, group_id)

        return Group(id=group_id, name=name)

    except Error as e:
        print("Error creating group:", e)
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_user_to_group(user_id, group_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='demo3db'
        )

        cursor = connection.cursor()

        # Add user to the group in the database
        query = "INSERT INTO user_groups (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, group_id))
        connection.commit()

        print("User added to group successfully.")

    except Error as e:
        print("Error adding user to group:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Mock user authorization function
def authorize_user(username, group):
    # Your authorization logic here
    if username == 'admin' and group == 'admin':
        return True
    else:
        return False
    
# Mock user authorization function
def authorize_user(username, path):
    # Your authorization logic here
    # Return True if user is authorized to access the path, False otherwise
    if username == 'admin' and path in ['/create_group', '/add_user_to_group']:
        return True
    elif username != 'admin' and path in ['/authenticate', '/register']:
        return True
    return False


# Middleware to authorize users
def authorize(func):
    def wrapper(self, *args, **kwargs):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Authentication required'}).encode('utf-8'))
            return
        encoded_credentials = auth_header[len('Basic '):].encode('utf-8')
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, _ = decoded_credentials.split(':', 1)
        if not authorize_user(username, self.path):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Unauthorized access'}).encode('utf-8'))
            return
        return func(self, *args, **kwargs)
    return wrapper
