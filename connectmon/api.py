from connectmon.logger import get_logger
from connectmon.models import Connector, Task, Message

from typing import List
import requests


class API:
    """API class for interacting with the Connect REST API

    Args:
        url (str): The URL of the Connect cluster

    Attributes:
        url (str): The URL of the Connect cluster
        logger (logging.Logger): The logger for this class
    """

    def __init__(self, url) -> None:
        self.url = url
        self.logger = get_logger(self.__class__.__name__)

    def __str__(self) -> str:
        return f"API(url={self.url})"

    def __repr__(self) -> str:
        return self.__str__()

    def is_reachable(self) -> bool:
        """Check if the Connect cluster is reachable

        Returns:
            bool: True if the cluster is reachable, False otherwise
        """
        self.logger.debug(f"Checking health of {self.url}")
        return requests.get(f"{self.url}/").status_code == 200

    def get_all_connector_status(self) -> List[Connector]:
        """Get the status of all connectors

        Returns:
            List[Connector]: A list of Connector objects
        """
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
        """Resume a paused connector

        Args:
            connector (Connector): The connector to resume

        Returns:
            requests.Response: The response from the API
        """
        self.logger.debug(f"Resuming {connector.name}")
        return requests.put(f"{self.url}/connectors/{connector.name}/resume")

    def restart_connector(self, connector: Connector) -> requests.Response:
        """Restart a failed connector

        Args:
            connector (Connector): The connector to restart

        Returns:
            requests.Response: The response from the API
        """
        self.logger.debug(f"Restarting {connector.name}")
        return requests.post(f"{self.url}/connectors/{connector.name}/restart")

    def restart_task(self, connector: Connector, task: Task) -> requests.Response:
        """Restart a failed task

        Args:
            connector (Connector): The connector the task belongs to
            task (Task): The task to restart

        Returns:
            requests.Response: The response from the API
        """
        self.logger.debug(f"Restarting task {task.id} for {connector.name}")
        return requests.post(
            f"{self.url}/connectors/{connector.name}/tasks/{task.id}/restart"
        )

    def restart_failed_connectors_if_any(
        self, connectors: List[Connector]
    ) -> List[Message]:
        """Restart failed connectors and tasks

        Args:
            connectors (List[Connector]): A list of Connector objects

        Returns:
            List[Message]: A list of errors and warning messages
        """
        errors_and_warnings = []

        for connector in connectors:
            self.logger.info(f"Checking {connector.name}...")

            if not connector.is_running:
                if connector.is_paused:
                    msg = Message(
                        sender=connector.name,
                        level="warn",
                        message=f"Resuming {connector.name}",
                    )
                    self.logger.warn(msg.message)
                    errors_and_warnings.append(msg)
                    self.resume_connector(connector)
                else:
                    msg = Message(
                        sender=connector.name,
                        level="error",
                        message=f"Restarting {connector.name}",
                    )
                    self.logger.error(msg.message)
                    errors_and_warnings.append(msg)
                    self.restart_connector(connector)

            for task in connector.tasks:
                if not task.is_running:
                    msg = Message(
                        sender=connector.name,
                        level="error",
                        message=f"Restarting task {task.id} for {connector.name}",
                    )
                    self.logger.error(msg.message)
                    errors_and_warnings.append(msg)
                    self.restart_task(connector, task)

        return errors_and_warnings


if __name__ == "__main__":
    from connectmon.env import env

    api = API(env.CONNECT_URL)
    print(api.is_reachable())
    print(api.get_connector_status("my-file-sink"))
    print(api.get_all_connector_status())
