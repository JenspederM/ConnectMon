from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class States:
    @property
    def is_running(self) -> bool:
        return self.state == "RUNNING"

    @property
    def is_paused(self) -> bool:
        return self.state == "PAUSED"

    @property
    def is_failed(self) -> bool:
        return self.state == "FAILED"


class ChannelActions(str, Enum):
    RESTART_FAILED = "RESTART_FAILED"
    RESTART_FAILED_CONNECTORS = "RESTART_FAILED_CONNECTORS"
    RESTART_FAILED_TASKS = "RESTART_FAILED_TASKS"
    RESUME_PAUSED_CONNECTORS = "RESUME_PAUSED_CONNECTORS"


class Channel(BaseModel):
    name: str
    type: str
    url: str
    actions: Optional[List[ChannelActions]] = [
        "RESTART_FAILED_CONNECTORS",
        "RESTART_FAILED_TASKS",
        "RESUME_PAUSED_CONNECTORS",
    ]
    include: Optional[List[str]] = ["*"]
    exclude: Optional[List[str]] = []


class Channels(BaseModel):
    channels: List[Channel]


class Message(BaseModel):
    """Represents a message from the API

    Args:
        sender (str): The sender of the message
        level (str): The level of the message
        message (str): The message

    Attributes:
        sender (str): The sender of the message
        level (str): The level of the message
        message (str): The message
    """

    sender: str
    level: str
    message: str


class Messages(BaseModel):
    connector_errors: List[Message] = []
    connector_warnings: List[Message] = []
    task_errors: List[Message] = []

    def __len__(self) -> int:
        return (
            len(self.connector_errors)
            + len(self.connector_warnings)
            + len(self.task_errors)
        )

    def add_connector_error(self, msg: Message):
        self.connector_errors.append(msg)

    def add_connector_warning(self, msg: Message):
        self.connector_warnings.append(msg)

    def add_task_error(self, msg: Message):
        self.task_errors.append(msg)


class Task(BaseModel, States):
    """Represents a task in a connector

    Args:
        id (int): The task id
        state (str): The task state
        worker_id (str): The worker id

    Attributes:
        id (int): The task id
        state (str): The task state
        worker_id (str): The worker id
        is_running (bool): True if the task is running
        is_failed (bool): True if the task is failed
        is_paused (bool): True if the task is paused
    """

    id: int
    state: str
    worker_id: str


class Connector(BaseModel, States):
    """Represents a connector

    Args:
        name (str): The name of the connector
        type (str): The type of the connector
        state (str): The state of the connector
        worker_id (str): The worker id of the connector
        tasks (list): A list of Task objects

    Attributes:
        name (str): The name of the connector
        type (str): The type of the connector
        state (str): The state of the connector
        worker_id (str): The worker id of the connector
        tasks (list): A list of Task objects
        is_running (bool): True if the connector is running
        is_failed (bool): True if the connector is failed
        is_paused (bool): True if the connector is paused
    """

    name: str
    state: str
    worker_id: str
    tasks: list
    type: str
