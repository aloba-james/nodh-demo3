from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str

@dataclass
class Group:
    id: int
    name: str