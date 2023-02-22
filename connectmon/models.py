from pydantic import BaseModel


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

    def __str__(self) -> str:
        return f"Message(message={self.message}, code={self.code})"

    def __repr__(self) -> str:
        return self.__str__()


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

    def __str__(self) -> str:
        return f"Task(id={self.id}, state={self.state}, worker_id={self.worker_id})"

    def __repr__(self) -> str:
        return self.__str__()


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

    def __str__(self) -> str:
        return f"Connector(name={self.name}, type={self.type} is_running={self.is_running}, state={self.state}, worker_id={self.worker_id}, tasks={self.tasks})"

    def __repr__(self) -> str:
        return self.__str__()
