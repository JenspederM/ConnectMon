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
from connectmon.config import settings
from connectmon.api import API

from pprint import pprint

## Setup your API you can get your environment variables from connectmon.config.settings
connect = API(settings.CONNECT_URL)

if not connect.is_reachable():
    raise Exception("Cluster is not reachable")

## Get a list of connectors and their status
connectors = connect.get_all_connector_status()

## Restart any failed or paused connectors and collect messages along the way
errors_and_warning = connect.restart_failed_connectors_if_any(connectors)

## If any channels have been registered in the configuration supplied through CONFIG_PATH 
## And there were any connectors or tasks to reset
## Then process each channel
if settings.CHANNELS and len(errors_and_warnings) > 0:
    for channel in settings.CHANNELS.channels:
        
        if channel.type == "teams":
            print(f"Sending message to {channel.name}...")
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
    include:
        - i-want-to-monitor-this-connector
        - this-too
    exclude:
        - who-cares-about-this-connector
        - this-is-someone-elses-problem
```

> Current only Microsoft Teams is supported. More will come if requested.