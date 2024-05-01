from getpass import getpass
from mysql.connector import connect, Error

create_users_table_query = """
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        password VARCHAR(100)
    )
"""

db_user = input("Enter username: ")
db_password = getpass("Enter password: ")

try:
    with connect(
        host="127.0.0.1",
        user=db_user,
        password=db_password,
        database="demo3db",
    ) as connection:
        # create_db_query = "CREATE DATABASE demo3db"
        # show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            # cursor.execute(create_db_query)
            # cursor.execute(show_db_query)
            # for db in cursor:
            #     print(db)
            cursor.execute(create_users_table_query)
            connection.commit()

except Error as e:
    print(e)

