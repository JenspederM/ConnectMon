from connectmon import env, API
from connectmon.utils import create_dummy_connectors
from connectmon.messaging import TeamsService


def main():
    ## Setup Kafka Connect Rest API client and check if cluster is reachable
    connect = API(env.CONNECT_URL)

    ## Get all connectors and check if any are in a failed state
    connectors = connect.get_all_connectors()
    # connectors = create_dummy_connectors(10)

    ## Loop through all channels and send a message if any connectors are in a failed state
    for channel in env.CHANNELS.channels:
        if channel.type == "teams":
            service = TeamsService(connect, channel)
            service.process_channel_connectors(connectors)
            service.send_message()


if __name__ == "__main__":
    main()
