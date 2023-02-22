from connectmon import env, API
from connectmon.logger import logger
from connectmon.utils import (
    create_dummy_connectors,
    process_channel_connectors,
    send_channel_messages,
)


def main():
    ## Setup Kafka Connect Rest API client and check if cluster is reachable
    connect = API(env.CONNECT_URL)

    if not env.CHANNELS:
        raise Exception("No channels defined")

    ## Get all connectors and check if any are in a failed state
    connectors = create_dummy_connectors(10)  # connect.get_all_connectors()

    for channel in env.CHANNELS.channels:
        logger.info(f"Processing channel {channel.name}...")

        # Process connectors and collect messages
        messages = process_channel_connectors(connect, channel, connectors)

        # Send messages to channel
        send_channel_messages(channel, messages)


if __name__ == "__main__":
    main()
