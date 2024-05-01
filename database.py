from getpass import getpass
from mysql.connector import connect, Error


create_users_table_query = """
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        password VARCHAR(100)
    )
"""

create_groups_table_query = """
    CREATE TABLE IF NOT EXISTS groups (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
"""
create_group_users_table_query = """
    CREATE TABLE group_users (
        group_id INT,
        user_id INT,
        PRIMARY KEY (group_id, user_id),
        FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
"""

create_filelist_table_query = """
    CREATE TABLE entfilelist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_url VARCHAR(255) NOT NULL
    );
"""


db_user = input("Enter username: ")
db_password = getpass("Enter password: ")


# Define your connection parameters
db_config = {
    'user': 'db_user',
    'password': 'db_password',
    'host': 'localhost',
    'database': 'demo3db'
}

try:
    with connect(
        **db_config
    ) as connection:
        # create_db_query = "CREATE DATABASE demo3db"

        with connection.cursor() as cursor:
            # atomic transaction
            # with connection.cursor() as cursor:
            #     cursor.execute(create_users_table_query)
            #     cursor.execute(create_groups_table_query)
            #     cursor.execute(create_group_users_table_query)
            #     connection.commit()
            # cursor.execute(create_db_query)

            # for db in cursor:
            #     print(db)
            # cursor.execute(create_users_table_query)

            with connection.cursor() as cursor:
                cursor.execute(create_users_table_query)
                cursor.execute(create_groups_table_query)
                cursor.execute(create_group_users_table_query)
                cursor.execute(create_filelist_table_query)
            connection.commit()

except Error as e:
    print(e)
