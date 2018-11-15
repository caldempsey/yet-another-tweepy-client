import click

from yatc import settings
from yatc.client import StreamingClient

HELP = """An application which implements a variety of consumers to return Twitter data."""
KEYS_HELP = """Validates whether configuration contains expected keys."""
CONSUME_HELP = """Specify a consumer to begin ingesting data."""


@click.group(help=HELP)
@click.pass_context
def cli(ctx):
    ctx.obj = StreamingClient()


@cli.command(help=KEYS_HELP)
def keys():
    return click.echo(settings.validate_json_config())


@cli.command(help=CONSUME_HELP)
@click.option("--type", "-t", help="Supports 'base' and 'stdout'.", default="", required=True)
@click.option("--mode", "-m", help="Supports 'filter' only.", required=True)
@click.pass_context
def consumer(ctx, type: str, mode: str):
    try:
        ctx.obj.hook_consumer(type, mode)
    except NotImplementedError:
        return click.echo("Sorry, this feature is not implemented right now. Come back soon!", err=True)


# Click mutator to allow "undefined options" to be passed (so we can pass kwargs from the CLI).
if __name__ == "__main__":
    cli()
