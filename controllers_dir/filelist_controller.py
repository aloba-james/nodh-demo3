import mysql.connector
from dataclasses import asdict
from schema import EntFilelist

db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="demo3db"
)
cursor = db.cursor()


class FileListController:
    @staticmethod
    def create_filelist(filelist):
        query = "INSERT INTO filelist (name, description, created_by, created_at, latest_version) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (filelist.name, filelist.description,
                       filelist.created_by, filelist.created_at, filelist.latest_version))
        db.commit()

    @staticmethod
    def get_filelist(filelist_id):
        query = "SELECT id, name, description, created_by, created_at, latest_version FROM filelist WHERE id = %s"
        cursor.execute(query, (filelist_id,))
        filelist_data = cursor.fetchone()
        if filelist_data:
            return EntFilelist(*filelist_data)
        else:
            return None

    @staticmethod
    def update_filelist(filelist):
        query = "UPDATE filelist SET name = %s, description = %s, latest_version = %s WHERE id = %s"
        cursor.execute(query, (filelist.name, filelist.description,
                       filelist.latest_version, filelist.id))
        db.commit()
    @staticmethod
    def delete_filelist(filelist_id):
        query = "DELETE FROM filelist WHERE id = %s"
        cursor.execute(query, (filelist_id,))
        db.commit()
