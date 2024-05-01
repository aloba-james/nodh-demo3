from mysql.connector import connect, Error
from schema import EntDataset
from database import db_config

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="dataset_storage"
)
cursor = db.cursor()


class DatasetController:
    @staticmethod
    def create_dataset(data):
        name = data.name
        description = data.description
        created_by = data.created_by
        created_at = data.created_at
        dataset = data.dataset

        query = "INSERT INTO dataset (name, description, created_by, created_at, data) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, description,
                       created_by, created_at, dataset))
        db.commit()

    @staticmethod
    def get_all_datasets():
        query = "SELECT id, name, description, created_by, created_at FROM dataset"
        cursor.execute(query)
        datasets = cursor.fetchall()

        results = []
        for dataset in datasets:
            ent_dataset = EntDataset(*dataset)
            results.append(ent_dataset)

        return results

    @staticmethod
    def get_dataset(dataset_id):
        query = "SELECT name, description, created_by, created_at, data FROM dataset WHERE id = %s"
        cursor.execute(query, (dataset_id,))
        dataset = cursor.fetchone()

        if dataset:
            ent_dataset = EntDataset(*dataset)
            return ent_dataset
        else:
            return None

    @staticmethod
    def update_dataset(data):
        dataset_id = data.id
        name = data.name
        description = data.description
        created_by = data.created_by
        created_at = data.created_at
        dataset = data.dataset

        query = "UPDATE dataset SET name = %s, description = %s, created_by = %s, created_at = %s, data = %s WHERE id = %s"
        cursor.execute(query, (name, description, created_by,
                       created_at, dataset, dataset_id))
        db.commit()

    @staticmethod
    def delete_dataset(dataset_id):
        query = "DELETE FROM dataset WHERE id = %s"
        cursor.execute(query, (dataset_id,))
        db.commit()
