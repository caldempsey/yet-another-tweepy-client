Yet Another Tweepy Client
---

A client implementing various producers designed to listen to data from the Twitter Streaming API.

# Installation

Right now we have no further support for secrets (since I've only spent, about two hours on this), so make sure you set a secrets config `.keys.json` in secrets according to the specification in the README. This will contain the details for your streaming API.

Currently the only producer is the STDOut producer which will pass all consumer input to standard output.

All errors (right now) are just logged to STDErr. 

Example Secrets Format.
==

# Legend

String: an str object

```
{
  "ENVIRONMENT": { // Specified in an environment variable.
    "CONSUMER_KEY": String, // Twitter Consumer Key.
    "CONSUMER_SECRET": String, // Twitter Consumer Secret.
    "ACCESS_TOKEN": String, // Twitter Access Token.
    "ACCESS_SECRET": String // Twitter Access Secret. 
  }
}

```

Creating Scripts 
===

You can also use all the useful abstractions to help create scripts! 

Settings.py provides helper functions to help take care of authentication for your users, while the YATC assembly of consumers will provide all the extra implementation details and documentation you need to get going quickly! Feel free to browse the example `weather_sentiment` scripts provided.

ToDo
---

Write unit tests for scripts (though they have been black box tested).