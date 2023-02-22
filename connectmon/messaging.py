from connectmon.models import Connector, Messages, Message, ChannelActions
from connectmon.logger import get_logger

from abc import ABC, abstractmethod
from typing import List
import pymsteams


class MessagingService(ABC):
    def __init__(self, api, channel) -> None:
        self.messages = Messages()
        self.api = api
        self.channel = channel
        self.logger = get_logger(self.__class__.__name__)

    def handle_failed_connector(self, connector: Connector):
        """Handle failed connectors

        Args:
            connector (Connector): The connector object

        Returns:
            None
        """
        if (
            ChannelActions.RESTART_FAILED in self.channel.actions
            or ChannelActions.RESTART_FAILED_CONNECTORS in self.channel.actions
        ):
            self.api.restart_connector(connector)
            level = "info"
            msg = f"Restarting {connector.name}"
        else:
            level = "error"
            msg = f"{connector.name} is not running, skipping restart"
            self.logger.info(msg)

        self.messages.add_connector_error(
            Message(sender=connector.name, level=level, message=msg)
        )

    def handle_paused_connector(self, connector: Connector):
        """Handle paused connectors

        Args:
            connector (Connector): The connector object

        Returns:
            None
        """
        if ChannelActions.RESUME_PAUSED_CONNECTORS in self.channel.actions:
            self.api.resume_connector(connector)
            level = "info"
            msg = f"Resuming {connector.name}"
        else:
            level = "warn"
            msg = f"{connector.name} is paused, skipping resume"
            self.logger.info(msg)

        self.messages.add_connector_warning(
            Message(sender=connector.name, level=level, message=msg)
        )

    def handle_failed_tasks(self, connector: Connector):
        """Handle failed tasks for a connector

        Args:
            connector (Connector): The connector object

        Returns:
            None
        """
        for task in connector.tasks:
            if task.is_failed:
                if (
                    ChannelActions.RESTART_FAILED in self.channel.actions
                    or ChannelActions.RESTART_FAILED_TASKS in self.channel.actions
                ):
                    self.api.restart_task(connector, task)
                    level = "info"
                    msg = f"Restarting task {task.id} for {connector.name}"
                else:
                    level = "error"
                    msg = f"Task {task.id} for {connector.name} is not running, skipping restart"
                    self.logger.info(msg)

                self.messages.add_task_error(
                    Message(sender=connector.name, level=level, message=msg)
                )

    def is_connector_included(self, connector: Connector) -> bool:
        """Check if a connector is included in the channel

        Args:
            connector (Connector): The connector object

        Returns:
            bool: True if the connector is included, False otherwise
        """
        return (
            # If include is empty, include all connectors
            len(self.channel.include) == 0
            # If include is *, include all connectors
            or "*" in self.channel.include
            # If include contains the connector name, include the connector
            or connector.name in self.channel.include
        )

    def process_channel_connectors(self, connectors: List[Connector]) -> None:
        """Process the connectors for a channel

        Args:
            connectors (List[Connector]): A list of Connector objects

        Returns:
            None
        """
        self.logger.info(f"Processing connectors for channel {self.channel.name}")

        for connector in connectors:
            is_included = self.is_connector_included(connector)

            if connector.name in self.channel.exclude:
                self.logger.info(f"Excluding {connector.name}...")
                continue
            elif not is_included:
                self.logger.info(f"{connector.name} is not included...")
                continue

            if is_included:
                if connector.is_failed:
                    self.handle_failed_connector(connector)
                elif connector.is_paused:
                    self.handle_paused_connector(connector)

                self.handle_failed_tasks(connector)

    @abstractmethod
    def build_message(self) -> any:
        """Build a message for the messaging service

        Returns:
            any: The message object
        """
        pass

    @abstractmethod
    def send_message(self) -> None:
        """Send a message to the messaging service

        Returns:
            None
        """
        pass


class TeamsService(MessagingService):
    def __init__(self, api, channel) -> None:
        super().__init__(api, channel)

    def add_section(
        self, card: pymsteams.connectorcard, title: str, messages: List[Message]
    ) -> None:
        """Add a section to a pymsteams connectorcard

        Args:
            card (pymsteams.connectorcard): The pymsteams connectorcard object
            title (str): The title of the section
            messages (List[Message]): A list of Message objects
        """
        self.logger.debug(f"Adding section {title} to card")
        section = pymsteams.cardsection()
        section.title(title)

        for msg in messages:
            section.addFact(msg.level, msg.message)

        card.addSection(section)

    def build_message(self) -> pymsteams.connectorcard:
        """Build a message for Microsoft Teams

        Args:
            webhook_url (str): The webhook url
            messages (List[dict]): A list of messages

        Returns:
            pymsteams.connectorcard: A pymsteams connectorcard object
        """
        self.logger.debug("Building Teams message")
        card = pymsteams.connectorcard(self.channel.url)
        card.title("ConnectMon Report")
        card.summary("Connector Monitor Summary")

        if self.messages.connector_errors:
            self.add_section(card, "Connector Errors", self.messages.connector_errors)

        if self.messages.connector_warnings:
            self.add_section(
                card, "Connector Warnings", self.messages.connector_warnings
            )

        if self.messages.task_errors:
            self.add_section(card, "Task Errors", self.messages.task_errors)

        return card

    def send_message(self):
        card = self.build_message()
        card.send()
        self.logger.info("Sent message to Teams")
