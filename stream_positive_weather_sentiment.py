# Example script on how to use the suite of Tweepy compliant to build scripts
# Particularly helpful for NiFi when we don't want any extra STDOut.
import sys

from tweepy import Stream, OAuthHandler

from yatc import settings
from yatc.consumers import STDConsumer
from yatc.settings import validate_json_config

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
    Stream(auth, STDConsumer(null_delimit=True)).filter(track=["\"weather\" :)"])
sys.exit(1)
