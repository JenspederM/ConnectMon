from connectmon.models import Connector, Task, Messages, Message, Channel
from connectmon.api import API
from connectmon.logger import get_logger

from typing import List
import pymsteams
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


def add_section(card: pymsteams.connectorcard, title: str, messages: List[Message]):
    """Add a section to a pymsteams connectorcard

    Args:
        card (pymsteams.connectorcard): The pymsteams connectorcard object
        title (str): The title of the section
        messages (List[Message]): A list of Message objects
    """
    logger.debug(f"Adding section {title} to card")
    section = pymsteams.cardsection()
    section.title(title)

    for msg in messages:
        section.addFact(msg.level, msg.message)

    card.addSection(section)


def build_teams_message(
    webhook_url: str, messages: Messages
) -> pymsteams.connectorcard:
    """Build a message for Microsoft Teams

    Args:
        webhook_url (str): The webhook url
        messages (List[dict]): A list of messages

    Returns:
        pymsteams.connectorcard: A pymsteams connectorcard object
    """
    logger.debug("Building Teams message")
    card = pymsteams.connectorcard(webhook_url)
    card.title("ConnectMon Report")
    card.summary("Connector Monitor Summary")

    if messages.connector_errors:
        add_section(card, "Connector Errors", messages.connector_errors)

    if messages.connector_warnings:
        add_section(card, "Connector Warnings", messages.connector_warnings)

    if messages.task_errors:
        add_section(card, "Task Errors", messages.task_errors)

    return card


def process_channel_connectors(
    connect: API, channel: Channel, connectors: List[Connector]
) -> Messages:
    """Process the connectors for a channel

    Args:
        connect (API): The Connect API object
        channel (Channel): The channel object
        connectors (List[Connector]): A list of Connector objects

    Returns:
        Messages: A Messages object
    """
    logger.info(f"Processing connectors for channel {channel.name}")
    messages = Messages()

    for connector in connectors:
        if connector.name in channel.exclude:
            logger.info(f"Skipping {connector.name}...")
            continue

        if "*" in channel.include or connector.name in channel.include:
            if connector.is_failed:
                msg = Message(
                    sender=connector.name,
                    level="error",
                    message=f"Restarting {connector.name}",
                )
                connect.restart_connector(connector)
                messages.add_connector_error(msg)
            elif connector.is_paused:
                msg = Message(
                    sender=connector.name,
                    level="warn",
                    message=f"Resuming {connector.name}",
                )
                connect.resume_connector(connector)
                messages.add_connector_warning(msg)

            for task in connector.tasks:
                if task.is_failed:
                    msg = Message(
                        sender=connector.name,
                        level="error",
                        message=f"Restarting task {task.id} for {connector.name}",
                    )
                    connect.restart_task(connector, task)
                    messages.add_task_error(msg)

    return messages


def send_channel_messages(channel: Channel, messages: Messages):
    """Send messages to a channel

    Args:
        channel (Channel): The channel object
        messages (Messages): A Messages object
    """
    logger.info(f"Sending messages for '{channel.type}' channel '{channel.name}'")
    if len(messages) > 0:
        if channel.type == "teams":
            teams_msg = build_teams_message(channel.url, messages)
            teams_msg.send()
