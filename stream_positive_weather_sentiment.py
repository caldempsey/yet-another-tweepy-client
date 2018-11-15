# Example script on how to use the suite of Tweepy compliant to build scripts
# Particularly helpful for NiFi when we don't want any extra STDOut.
import json
import sys

from tweepy import Stream, OAuthHandler, StreamListener

from yatc import settings
from yatc.consumers import STDConsumer
from yatc.settings import validate_json_config


# Override to extract only meaningful metadata
class SentimentConsumer(StreamListener):
    """
    A TweetConsumer is responsible for listening to a Tweepy stream and ingesting its data.
    The Base Consumer is responsible only for returning data (tweets) ingested and can be hooked onto.
    """

    def __init__(self):
        """
        Initialises the consumer, inherits from Tweepy Stream Listener. Achieves nothing more than returns data directly
        to processes hooked onto the function.
        """
        super().__init__()

    def on_data(self, data):
        """
        Override from the Tweepy on_data documentation.
        """
        # Load JSON into keys to extract values
        data = json.loads(data)
        # Dump data output with expected vars, we are interested in locations we do know about, and we are not
        # interested in retweeted data.
        if not (data["retweeted"]) and not (data["coordinates"] is None):
            print("\x00" + json.dumps({"id": data["id"], "text": data["text"], "positive_sentiment": True}))
        return True

    def on_error(self, status):
        """
        Override from the Tweepy on_error documentation.
        """
        if status == 420:
            # Returning false will disconnect the stream.
            return False
        return True


# Check to see if the secrets stored in configuration variables are valid otherwise terminate the script.
if not validate_json_config:
    raise ValueError("Please ensure YATC configuration files are correctly formatted.")
else:
    # Get secrets from JSON.
    secrets = settings.get_dict_secrets()
    # Retrieve authentication variables.
    auth = OAuthHandler(secrets["consumer_key"], secrets["consumer_secret"])
    auth.set_access_token(secrets["access_token"], secrets["access_secret"])
    # Get an STDConsumer object which we will use to delimit JSON responses, and pass that to a Tweepy Stream object.
    # Use Twitters sentiment analysis engine to determine the results.
    Stream(auth, SentimentConsumer()).filter(track=["weather :)"])
sys.exit(1)
