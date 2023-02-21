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
from connectmon.utils import build_teams_message

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
        print(f"Sending message to {channel.name}...")
        if channel.type == "teams":
            teams_msg = build_teams_message(channel.url, errors_and_warnings)
            teams_msg.send()
```

## Configuration
| Name | Type | Description |
|------|------|-------------|
| CONNECT_URL | string | The URL of the Connect cluster |
| ENVIRONMENT | string | The environment the application is running in |
| LOG_LEVEL | string | The log level for the application |
| LOG_FORMAT | string | The log format for the application |
| CONFIG_PATH | Optional string | The path to the configuration file |

If `CONFIG_PATH` is provided, the application will attempt to load
configuration from the file, which will set `settings.CHANNELS` with the
channels configured in the supplied configuration file.

A config file could look like this
```yaml
channels:
  - name: my-teams-team-name
    type: teams
    url: https://my-org.webhook.office.com/webhookb2/...

```

Possible future?:
```yaml
channels:
  - name: my-teams-team-name
    type: teams
    url: https://my-org.webhook.office.com/webhookb2/...
    include:
        - i-want-to-monitor-this-connector
        - this-too
    exclude:
        - who-cares-about-this-connector
        - this-is-someone-elses-problem
```

> Current only Microsoft Teams is supported. More will come if requested.