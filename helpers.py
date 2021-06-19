import settings
from slack import WebClient
from slack.errors import SlackApiError

def post_chat_to_slack(message):
	"""
	Posts a message to slack.
	"""
	
	client = WebClient(token=settings.SLACK_TOKEN)
	try:
		# Post a message to slack
		response = client.chat_postMessage(
			text=message,
			channel=settings.SLACK_CHANNEL,
			unfurl_links=True,
			unfurl_media=True
		)
		
	except SlackApiError as e:
		assert e.response["error"]
		print("Got an error: " + e.response['error'])