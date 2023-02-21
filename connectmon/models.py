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


class Task(States):
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

    def __init__(self, id, state, worker_id) -> None:
        self.id: int = id
        self.state: str = state
        self.worker_id: str = worker_id

    def __str__(self) -> str:
        return f"Task(id={self.id}, state={self.state}, worker_id={self.worker_id})"

    def __repr__(self) -> str:
        return self.__str__()


class Connector(States):
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

    def __init__(
        self,
        name: str,
        type: str,
        state: str,
        worker_id: str,
        tasks: list,
    ) -> None:
        self.name: str = name
        self.state: str = state
        self.worker_id: str = worker_id
        self.tasks: list = tasks
        self.type: str = type

    def __str__(self) -> str:
        return f"Connector(name={self.name}, type={self.type} is_running={self.is_running}, state={self.state}, worker_id={self.worker_id}, tasks={self.tasks})"

    def __repr__(self) -> str:
        return self.__str__()
