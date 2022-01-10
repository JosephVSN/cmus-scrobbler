#!/usr/bin/python
"""Console script for cmus_scrobbler."""
import cmus_scrobbler
import argparse
import sys

def main():
    """Console script for cmus_scrobbler."""
    parser = argparse.ArgumentParser()
    parser.add_argument('status', nargs='*')
    parser.add_argument('-c', '--config', nargs=2, help="Called with the API KEY and API SECRET KEY as arguments, updates their values in the config.")
    args = parser.parse_args()
    return cmus_scrobbler.main(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
