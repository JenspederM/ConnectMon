from connectmon.models import Connector, Task
from connectmon.logger import get_logger

from typing import List
import random

logger = get_logger("utils")


def create_dummy_connectors(n: int) -> List[Connector]:
    """Create a list of dummy connectors

    Args:
        n (int): The number of connectors to create

    Returns:
        List[Connector]: A list of Connector objects
    """
    logger.debug(f"Creating {n} dummy connectors")

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
