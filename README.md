# ConnectMon

A tool for monitoring Kafka Connect. 

Provide a config file to describe where messages should be sent to. For example:
```
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

> Current only Microsoft Teams is supported.