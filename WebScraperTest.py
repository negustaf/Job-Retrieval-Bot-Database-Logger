from slack import WebClient
from WebScraper import WebScraperBot
import os

# Create a slack client.
slackWebClient = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Get new job postings.
runWebScraperBot = WebScraperBot('#job-retriever', 'product-designer', 'california')

# Get the onboarding message payload.
message = runWebScraperBot.getMessagePayload()

# Post the onboarding message in Slack.
slackWebClient.chat_postMessage(**message)