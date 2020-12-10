import re
import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from WebScraper import WebScraperBot

# Initialize a Flask app to host the events adapter.
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the Slack app for event ingestion.
slackEventsAdapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client.
slackWebClient = WebClient(token=os.environ.get("SLACK_TOKEN"))

# runWebScraperBot() creates a new WebScraperBot event and collects the message payload with the job position data. Then it sends the onboarding message to Slack to post.
def runWebScraperBot(slackChannel, keyword, locale):
    runWebScraper = WebScraperBot(slackChannel, keyword, locale)
    message = runWebScraper.getMessagePayload()
    slackWebClient.chat_postMessage(**message)

# When a "message" event is detected by the events adapter, forward the payload to this function. @slackEventsAdapter.on("message") allows message() to receive events.
@slackEventsAdapter.on('message')

# message() (1) parses the message event and (2) if the text contains (3) the activation string, (4) the channel ID that the event was executed on will be fetched and (5) execute runWebScraperBot and send the results to that channel.
def message(payload):
    event = payload.get('event', {})
    text = event.get('text')
    keyword = r'jobs\(([a-zA-Z1-9\s]*),\s[a-zA-z1-9\s]*\)'
    locale = r'jobs\([a-zA-Z1-9\s]*,\s([a-zA-z1-9\s]*)\)'
    activator = 'jobs({} in {})'.format(keyword, locale)
    if activator in text.lower():
        channelID = event.get('channel')
        return runWebScraperBot(channelID, keyword, locale)

# "logger" creates the logging object and set the log level to DEBUG. This increases verbosity of logging messages. It then adds StreamHandler() as a logging handler. The app then runs on the externally facing IP address on port 3000 instead of on localhost.
if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=3000)
