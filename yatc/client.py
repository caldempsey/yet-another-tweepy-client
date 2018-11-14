import codecs
import logging
import sys

from tweepy import OAuthHandler, Stream

from yatc import settings
from yatc.consumers import BaseConsumer, STDConsumer

log = logging.getLogger("Streams.client: ")


class StreamingClient:
    """
     The StreamingClient is responsible for setting up consumers according to the application configuration.
    """

    def __init__(self):
        """
        Initialises a Streaming client either from passed credentials or from local configuration.

        When uri, key, and .config is False, this function gets the credentials from the .config JSON file.
        """
        # Runtime execution to ensure config validity.
        try:
            if not settings.validate_json_config():
                raise KeyError()
        except KeyError:
            log.exception("Client will not connect until configuration has valid keys.")
        self.consumer = None

    def hook_consumer(self, type: str, mode: str):
        """
        Creates and returns an instance of a consumer determined by type.
        :param mode:
        :param type:
        :param kwargs: Keyword arguments containing at least "type" and "mode"
        """
        secrets = settings.get_dict_secrets()
        # Retrieve authentication variables.
        auth = OAuthHandler(secrets["consumer_key"], secrets["consumer_secret"])
        auth.set_access_token(secrets["access_token"], secrets["access_secret"])
        # Default consumer is a BaseConsumer which requires no special arguments.
        consumer = BaseConsumer()
        # Different kinds of consumers defined here. If a type is invalid pass back a ValueError.
        try:
            if type == "base" or type == "":
                pass
            elif type == "stdout":
                consumer = STDConsumer()
            else:
                raise ValueError()
        except ValueError:
            log.exception("Valid consumer type must be specified for a client connection.")
            raise
        # At this stage we have a consumer stored as a reference to the object. Now we need to tell the consumer what
        # it's supposed to be doing. We do this by getting relevant configuration from the JSON (settings.json) for a
        # particular "mode".
        config = settings.get_dict_config()
        # TODO Ways this could be improved is passing kwargs to allow user defined settings.
        if mode == "filter":
            self.consumer = Stream(auth, consumer).filter(track=config["track"])
        else:
            raise NotImplementedError()
        return self.consumer
