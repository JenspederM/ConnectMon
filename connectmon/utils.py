from connectmon.models import Connector, Task, Message

import pymsteams
import random

from typing import List


def create_dummy_connectors(n: int) -> List[Connector]:
    """Create a list of dummy connectors

    Args:
        n (int): The number of connectors to create

    Returns:
        List[Connector]: A list of Connector objects
    """
    samples = []

    for i in range(n):
        is_running = random.random() > 0.5
        is_failed = random.random() > 0.5

        connector = Connector(
            name=f"sample-{i}",
            type="source",
            state="FAILED" if is_failed else "RUNNING" if is_running else "PAUSED",
            worker_id=f"worker-{i}",
            tasks=[],
        )

        tasks = []
        for j in range(5):
            is_task_running = True if is_running else random.random() > 0.5

            tasks.append(
                Task(
                    id=j,
                    state="RUNNING" if is_task_running else "FAILED",
                    worker_id=f"worker-{j}",
                )
            )

        connector.tasks = tasks

        samples.append(connector)

    return samples


def build_teams_message(
    webhook_url: str, messages: List[Message]
) -> pymsteams.connectorcard:
    """Build a message for Microsoft Teams

    Args:
        webhook_url (str): The webhook url
        messages (List[dict]): A list of messages

    Returns:
        pymsteams.connectorcard: A pymsteams connectorcard object
    """
    msg = pymsteams.connectorcard(webhook_url)

    error_section = pymsteams.cardsection()
    error_section.title("Connector Errors")

    warn_section = pymsteams.cardsection()
    warn_section.title("Connector Warnings")

    task_section = pymsteams.cardsection()
    task_section.title("Task Errors")

    for message in messages:
        if message.level == "error" and "task" in message.message:
            task_section.addFact(f"{message.level}", f"{message.message}")
        elif message.level == "error":
            error_section.addFact(f"{message.level}", f"{message.message}")
        elif message.level == "warn":
            warn_section.addFact(f"{message.level}", f"{message.message}")

    msg.addSection(error_section)
    msg.addSection(warn_section)
    msg.addSection(task_section)

    msg.summary("Connector Monitor Summary")

    return msg
