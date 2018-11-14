import json
import logging
import os

log = logging.getLogger("Streams.settings: ")
path = os.path.dirname(__file__)
secret_keys = ["CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN", "ACCESS_SECRET"]
config_keys = ["locations", "track", "allow_retweets", "null_delimit"]
# TODO Parameterized path so you can specify the configuration in the UI.
default_secrets_path = os.path.join(os.path.dirname(__file__), ".config/keys.json")
default_config_path = config_keys_dir = os.path.join(os.path.dirname(__file__), "config/settings.json")


def _has_valid_secret_json(secrets: dict):
    if all(key in secret_keys for key in secrets):
        return True
    else:
        return False


def _has_valid_config_json(config: dict):
    if all(key in config_keys for key in config):
        return True
    else:
        return False


def validate_json_config() -> bool:
    """
    Validates the configuration specified in secrets and settings.

    :param env: Input configuration type for secrets (i.e. production or development).
     Expected to be a valid environment variable in the near future.
    :return: Returns a dictionary containing the following keys.

    consumer_key: the consumer key.
    consumer_secret: the consumer .config
    access_token: the access token.
    access_secret: the access .config.
    """
    with open(default_secrets_path) as json_secrets, \
            open(default_config_path) as json_config:
        try:
            # Load JSON.
            secrets = json.load(json_secrets)
            config = json.load(json_config)
            # Check if keys are valid.
            return _has_valid_secret_json(secrets) and _has_valid_config_json(config)
        except (FileNotFoundError, TypeError):
            log.exception("Settings detected as invalid JSON.")
            raise
        finally:
            json_secrets.close()
            json_config.close()


def _get_secrets_json():
    """
      Returns the secrets configuration in .keys.
      :return: Returns a dictionary containing the following keys.

      consumer_key: the consumer key.
      consumer_secret: the consumer secret
      access_token: the access token.
      access_secret: the access secret.
      """
    with open(default_secrets_path) as json_secrets:
        config_data = json.load(json_secrets)
        try:
            # Build a dict of API secret and keys.
            settings = {"consumer_key": config_data["CONSUMER_KEY"], "consumer_secret": config_data["CONSUMER_SECRET"],
                        "access_token": config_data["ACCESS_TOKEN"], "access_secret": config_data["ACCESS_SECRET"]}
        except (FileNotFoundError, KeyError, TypeError):
            log.exception("Keys file is invalid or has not been found.")
            raise
        else:
            return settings


def _get_config_json():
    """
      Returns the secrets configuration in .keys.
      :return: Returns a dictionary containing the following keys.

      consumer_key: the consumer key.
      consumer_secret: the consumer secret
      access_token: the access token.
      access_secret: the access secret.
      """
    with open(default_config_path) as json_config:
        config_data = json.load(json_config)
        try:
            # Build a dict of API keys.
            settings = {"allow_retweets": config_data["allow_retweets"], "track": config_data["track"],
                        "locations": config_data["locations"], "null_delimit": config_data["null_delimit"]}
        except (FileNotFoundError, KeyError, TypeError):
            log.exception("Config file is invalid or has not been found.")
            raise
        else:
            return settings


def prune_dict_secrets(config: dict):
    """
    Responsible for removing expected configuration arguments from a dict where secrets (i.e. access tokens) are stored for
    application safety. :param config: :return: Returns a pruned dictionary.
    """
    config.pop("consumer_key")
    config.pop("consumer_secret")
    config.pop("access_token")
    config.pop("access_secret")
    return config


def get_dict_secrets():
    """
    Responsible for returning secret values to be used throughout the application.
    config: :return: Returns a dictionary of secret configuration.
    """
    _get_secrets_json()
    return _get_secrets_json()


def get_dict_config():
    """
    Responsible returning values specified in JSON config.
    :param config: :return: Returns a dictionary of updated configuration.
    """
    return _get_config_json()
