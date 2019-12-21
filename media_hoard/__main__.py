# -*- coding: utf-8 -*-

"""Entry point for media_hoard."""

import argparse
import sys


def main():
    """Entry point for media_hoard."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "media_hoard.__main__.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
