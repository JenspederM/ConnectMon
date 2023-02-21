from connectmon.logger import get_logger
from connectmon.models import Connector, Task

from typing import List
import requests


class API:
    def __init__(self, url) -> None:
        self.url = url
        self.logger = get_logger(self.__class__.__name__)

    def __str__(self) -> str:
        return f"API(url={self.url})"

    def __repr__(self) -> str:
        return self.__str__()

    def is_healthy(self) -> requests.Response:
        return requests.get(f"{self.url}/").status_code == 200

    def get_all_connector_status(self) -> requests.Response:
        response = requests.get(f"{self.url}/connectors?expand=status")

        if response.status_code == 200:
            connector_statuses = response.json()

            connectors = []
            for value in connector_statuses.values():
                data = value["status"]
                tasks = []
                for task in data["tasks"]:
                    task = Task(**task)
                    tasks.append(task)

                connector = Connector(
                    name=data["name"],
                    type=data["type"],
                    state=data["connector"]["state"],
                    worker_id=data["connector"]["worker_id"],
                    tasks=tasks,
                )

                connectors.append(connector)

        return connectors

    def resume_connector(self, connector: Connector) -> requests.Response:
        self.logger.debug(f"Resuming {connector.name}")
        return requests.put(f"{self.url}/connectors/{connector.name}/resume")

    def restart_connector(self, connector: Connector) -> requests.Response:
        self.logger.debug(f"Restarting {connector.name}")
        return requests.post(f"{self.url}/connectors/{connector.name}/restart")

    def restart_task(self, connector: Connector, task: Task) -> requests.Response:
        self.logger.debug(f"Restarting task {task.id} for {connector.name}")
        return requests.post(
            f"{self.url}/connectors/{connector.name}/tasks/{task.id}/restart"
        )

    def restart_failed_connectors_if_any(self, connectors: List[Connector]):
        messages = []

        for connector in connectors:
            self.logger.info(f"Checking {connector.name}...")

            if not connector.is_running:
                if connector.is_paused:
                    msg = {"level": "warn", "message": f"Resuming {connector.name}"}
                    self.logger.warn(msg["message"])
                    messages.append(msg)
                    self.resume_connector(connector)
                else:
                    msg = {"level": "error", "message": f"Restarting {connector.name}"}
                    self.logger.error(msg["message"])
                    messages.append(msg)
                    self.restart_connector(connector)

            for task in connector.tasks:
                if not task.is_running:
                    msg = {
                        "level": "error",
                        "message": f"Restarting task {task.id} for {connector.name}",
                    }
                    self.logger.error(msg["message"])
                    messages.append(msg)
                    self.restart_task(connector, task)

        return messages


if __name__ == "__main__":
    from connectmon.config import settings

    api = API(settings.CONNECT_URL)
    print(api.is_healthy())
    print(api.get_connector_status("my-file-sink"))
    print(api.get_all_connector_status())
