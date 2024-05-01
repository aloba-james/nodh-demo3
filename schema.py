from dataclasses import dataclass, field
from enum import auto, Enum
from typing import List


ID = int


@dataclass
class User:
    id: ID
    username: str
    password: str

@dataclass
class Group:
    id: ID
    name: str

class Grouping(Enum):
    FILELIST = auto()
    LIST = auto()
    DATASET = auto()


class Action(Enum):
    ADD = auto()
    DELETE = auto()


class AuditAction(Enum):
    ACCESS = auto()
    MUTATE = auto()


class ObjectType(Enum):
    RECORDING = auto()
    FILELIST = auto()
    LIST = auto()
    DATASET = auto()


class Mode(Enum):
    FRONTEND = auto()
    LIBRARY = auto()
    CODE = auto()


@dataclass
class EntVersion:
    id: ID
    version_number: int
    grouping: Grouping  # DATASET, FILELIST or LIST
    object_id: id  # EntDataset, EntFileList or EntList
    created_by: id
    last_accessed: int
    last_accessed_by: id
    created_at: int
    description: str
    published: bool

    file_list_tags: List["EntFilelistVersionTag"] = field(
        default_factory=list, init=False, repr=False
    )


@dataclass
class EntTag:
    id: ID
    value: str
    description: str
    created_by: id
    created_at: int


@dataclass
class EntRecording:
    id: id
    dataset_id: id  # EntDataset
    parent_id: id  # EntRecording, this can be None, all augemeted recordings will have this field set
    name: str
    description: str
    created_by: id
    created_at: int
    location: str
    scene: str
    device_type: str
    duration: float
    augmented: bool
    muted: bool
    path: str

    tags: List["EntRecordingTag"] = field(default_factory=list, init=False, repr=False)


@dataclass
class EntRecordingTag:
    recording_id: id  # EntRecording
    tag_id: id  # EntTag
    created_by: id
    created_at: int


@dataclass
class EntDataset:
    id: id
    name: str
    description: str
    created_by: id
    created_at: int


@dataclass
class EntDatasetVersion:
    id: id
    dataset_id: id  # EntDataset, this could be removed as EntVersion already contains it, but left it for easy reference
    recording_id: id  # EntRecording
    version_id: id  # EntVersion
    action: Action  # ADD or DELETE, as database will only contain diff between versions
    created_by: id
    created_at: int
    description: str


@dataclass
class EntDatasetVersionTag:
    dataset_version_id: id  # EntVersion
    tag_id: id  # EntTag
    created_by: id
    created_at: int


@dataclass
class EntFilelist:
    id: id
    name: str
    description: str
    created_by: id
    created_at: int
    latest_version: int


@dataclass
class EntFilelistVersion:
    id: id
    filelist_id: id  # EntFileList, this could be removed as EntVersion already contains it, but left it for easy reference
    recording_id: id  # EntRecording
    version_id: id  # EntVersion
    action: Action  # ADD or DELETE, as database will only contain diff between versions
    created_by: id
    created_at: int
    description: str


@dataclass
class EntFilelistVersionTag:
    filelist_version_id: id  # EntVersion
    tag_id: id  # EntTag
    created_by: id
    created_at: int


@dataclass
class EntList:
    id: id
    name: str
    description: str
    created_by: id
    created_at: int
    latest_version: int


@dataclass
class EntListVersion:
    id: id
    list_id: id  # EntList, this could be removed as EntVersion already contains it, but left it for easy reference
    file_list_id: id  # EntFileList
    version_id: id  # EntVersion
    action: Action  # ADD or DELETE, as database will only contain diff between versions
    created_by: id
    created_at: int
    description: str


@dataclass
class EntListVersionTag:
    list_version_id: id  # EntVersion
    tag_id: id  # EntTag
    created_by: id
    created_at: int


@dataclass
class Model:
    id: id
    name: str
    description: str
    created_by: id
    created_at: int
    train_file_list_v: id  # EntVersion
    test_file_list_v: id  # EntVersion


@dataclass
class EntLexieAudit:
    id: id
    object_type: ObjectType  # RECORDING, FILELIST, LIST or DATASET
    object_id: id  # EntRecording, EntFileList, EntList or EntDataset
    version_id: id  # EntVersion
    created_by: id
    created_at: int
    action: AuditAction  # ACCESS or MUTATE
    mode: Mode  # FRONTEND, LIBRARY or CODE


@dataclass
class Annotations:
    id: id
    recording_id: id  # EntRecording
    start_time: float
    end_time: float
    description: str
    created_by: id
    created_at: float    