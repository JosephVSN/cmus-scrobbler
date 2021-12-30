"""Main module."""

import os
import config

def main(args) -> int:
    """
    Main handler for cmus_scrobbler
    Receives args as a Namespace from cli.py, and either starts generating an API call
    or updating the config, depending on how the CLI was called. Returns a 0 for success
    and a 1 for any non-nominal results.
    """
    if args.config:
        return int(config.update_config(*args.config))
    elif args.status:
        pass
    else:
        print("Couldn't figure out what the user was trying to do, try cmus-scrobbler --help!");
        return 1