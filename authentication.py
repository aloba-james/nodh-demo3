import mysql.connector
from mysql.connector import connect, Error
from user_schema import User
import getpass 
from api import db_password, db_user


def authenticate_user(username, password):
    try:
        with connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='demo3db'
        ) as connection:

            cursor = connection.cursor(dictionary=True)

            # Query the database for the user
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()

            if user_data:
                user = User(**user_data)
                return user
            else:
                return None

    except Error as e:
        print("Error authenticating user:", e)
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def register_user(username, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_password,
            database='demo3db'
        )

        cursor = connection.cursor()

        # Check if the username already exists
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Username already exists")
            return False

        # Create a new user record
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        connection.commit()

        print("User registered successfully.")
        return True

    except Error as e:
        print("Error registering user:", e)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
