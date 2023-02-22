# ConnectMon

A tool for monitoring tasks and connectors in Kafka Connect. 

## Installation

With pip
```
pip install connectmon
```

With poetry
```
poetry add connectmon
```

## Usage

```py
from connectmon import env, API
from connectmon.messaging import TeamsService


## Setup Kafka Connect Rest API client and check if cluster is reachable
connect = API(env.CONNECT_URL)

## Get all connectors and check if any are in a failed state
connectors = connect.get_all_connectors()

## Loop through all channels and send messages
for channel in env.CHANNELS.channels:
    if channel.type == "teams":
        service = TeamsService(connect, channel)
        service.process_channel_connectors(connectors)
        service.send_message()
```

## Configuration

Base configuration for ConnectMon is handled through Environment Variables. 

### Environment Variables

| Name | Type | Description | Default |
|------|------|-------------| ------- | 
 **CONFIG_PATH** | Optional string | The path to the channel configuration file | `""` |
 **CONNECT_URL** | string | The URL of the Connect cluster | `"http://localhost:8083"` |
 ENVIRONMENT | string | The environment the application is running in | `"dev"` |
 LOG_LEVEL | string | The log level for the application | `"INFO"` |
 LOG_FORMAT | string | The log format for the application | `"(asctime)s - ..."` |

> *Name in bold are required!*

If `CONFIG_PATH` is provided, the application will attempt to load
configuration from the file, which will set `settings.CHANNELS` with the
channels configured in the supplied configuration file.

### Channel Configuration

You can configure specific channels to receive notifications when connectors or tasks are paused or failed.

A config file could look like this

```yaml
channels:
  - name: my-teams-team-name
    type: teams
    url: https://my-org.webhook.office.com/webhookb2/...
    actions:
      - RESTART_FAILED
    include:
      - i-want-to-monitor-this-connector
      - this-too
    exclude:
      - who-cares-about-this-connector
      - this-is-someone-elses-problem
```

Supported fields for channels are:

| Name | Type | Description | Default |
| ---- | ---- | ----------- | ------- |
| **name** | string | Name of the channel | `""` |
| **type** | string | Type of channel | `""` |
| **url**  | string | Url to send payload to | `""` |
| actions | list of strings | Can be any of `RESTART_FAILED`, `RESTART_FAILED_CONNECTORS`, `RESTART_FAILED_TASKS`, `RESUME_PAUSED_CONNECTORS` | `RESTART_FAILED` |
| include | list of strings | Names of connectors to include for this channel | `["*"]` |
| exclude | list of strings | Names of connectors to *exclude* for this channel | `[]` |

> Current only Microsoft Teams or `type: "teams"` is supported.