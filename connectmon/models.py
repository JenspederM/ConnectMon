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
    def __init__(self, id, state, worker_id) -> None:
        self.id: int = id
        self.state: str = state
        self.worker_id: str = worker_id

    def __str__(self) -> str:
        return f"Task(id={self.id}, state={self.state}, worker_id={self.worker_id})"

    def __repr__(self) -> str:
        return self.__str__()


class Connector(States):
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
