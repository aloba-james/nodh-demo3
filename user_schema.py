# user_schema.py

from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str