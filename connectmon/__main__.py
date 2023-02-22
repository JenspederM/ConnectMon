from connectmon import env, API
from connectmon.logger import logger
from connectmon.utils import build_teams_message


def main():

    ## Setup Kafka Connect Rest API client and check if cluster is reachable
    connect = API(env.CONNECT_URL)

    if not connect.is_reachable():
        raise Exception("Cluster is not reachable")

    ## Get all connectors and check if any are in a failed state
    connectors = connect.get_all_connector_status()

    ## Restart failed connectors and tasks
    errors_and_warnings = connect.restart_failed_connectors_if_any(connectors)

    ## Send message to Teams channel if any errors or warnings
    if env.CHANNELS and len(errors_and_warnings) > 0:
        for channel in env.CHANNELS.channels:
            logger.info(f"Sending message to {channel.name}...")
            if channel.type == "teams":
                teams_msg = build_teams_message(channel.url, errors_and_warnings)
                teams_msg.send()


if __name__ == "__main__":
    main()
