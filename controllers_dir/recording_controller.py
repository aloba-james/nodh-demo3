import mysql.connector
from dataclasses import asdict
from typing import List
from schema import EntRecording

db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="dataset_storage"
)
cursor = db.cursor()

class RecordingController:
    @staticmethod
    def create_recording(recording):
        query = """
            INSERT INTO recording (dataset_id, parent_id, name, description, created_by, created_at, 
            location, scene, device_type, duration, augmented, muted, path, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (recording.dataset_id, recording.parent_id, recording.name,
                               recording.description, recording.created_by, recording.created_at,
                               recording.location, recording.scene, recording.device_type,
                               recording.duration, recording.augmented, recording.muted,
                               recording.path, recording.user_credentials.id))
        db.commit()

    @staticmethod
    def get_recordings(dataset_id):
        query = """
            SELECT id, dataset_id, parent_id, name, description, created_by, created_at, 
            location, scene, device_type, duration, augmented, muted, path, user_id
            FROM recording
            WHERE dataset_id = %s
        """
        cursor.execute(query, (dataset_id,))
        recordings_data = cursor.fetchall()
        recordings = [EntRecording(*recording) for recording in recordings_data]
        return recordings

    # Implement update, delete, and other methods as needed
