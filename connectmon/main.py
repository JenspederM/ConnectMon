from connectmon.config import settings
from connectmon.api import API
from connectmon.logger import get_logger
from connectmon.utils import build_teams_message, create_dummy_connectors

from pprint import pprint

logger = get_logger(__name__)


if __name__ == "__main__":
    ## Setup your API you can get your environment variables from connectmon.config.settings
    connect = API(settings.CONNECT_URL)

    if not connect.is_reachable():
        raise Exception("Cluster is not healthy")

    connectors = connect.get_all_connector_status()
    # connectors = create_dummy_connectors(10)

    pprint(connectors)

    errors_and_warnings = connect.restart_failed_connectors_if_any(connectors)

    if settings.CHANNELS and len(errors_and_warnings) > 0:
        pprint(errors_and_warnings)
        for channel in settings.CHANNELS.channels:
            logger.info(f"Sending message to {channel.name}...")
            if channel.type == "teams":
                teams_msg = build_teams_message(channel.url, errors_and_warnings)
                teams_msg.send()
