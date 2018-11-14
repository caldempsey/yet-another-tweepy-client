import logging

from tweepy.streaming import StreamListener

"""
Tweet consumers are responsible for listening to a stream of tweets (from Twitter) and ingesting their data.

All consumers have the option to print yatc to STD out (as overridable in settings.json). The STD out consumer is 
uniquely responsible for this, and slightly more optimised to the task. 
"""

log = logging.getLogger("Stream.TweetListeners: ")


class BaseConsumer(StreamListener):
    """
    A TweetConsumer is responsible for listening to a Tweepy stream and ingesting its data.
    The Base Consumer is responsible only for returning data (tweets) ingested and can be hooked onto.
    """

    def __init__(self, **kwargs):
        """
        Initialises the consumer, inherits from Tweepy Stream Listener. Achieves nothing more than returns data directly
        to processes hooked onto the function.
        """
        super().__init__()

    def on_data(self, data):
        """
        Override from the Tweepy on_data documentation.
        """
        # Returning True (or returning a truthy value, that is not false) continues the stream.
        return data

    def on_error(self, status):
        """
        Override from the Tweepy on_error documentation.
        """
        log.exception("Consumer threw Twitter status code: " + str(status))
        if status == 420:
            # Returning false will disconnect the stream.
            return False
        return True


class STDConsumer(BaseConsumer):
    """
    The STDOut is responsible for listening to a Tweepy stream and printing Tweet output to standard output.
    """

    def __init__(self):
        """
        Initialises the consumer, inherits from Tweepy Stream Listener.
        """
        # To prevent encoding errors (charmap codec errors, etc) in the stdout stream
        super().__init__()

    def on_data(self, data):
        """
        Override from the Tweepy on_data documentation. Prints JSON responses to stdout as they arrive.
        """
        print(data)
        # Returning True (or returning a truthy value, that is not false) continues the stream.
        return True
