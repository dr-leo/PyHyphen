import argparse
import sys

import textwrap2
from hyphen import Hyphenator


def main():
    parser = argparse.ArgumentParser(
        description="Wrap text file to given width, with hyphenation"
    )
    parser.add_argument("-w", "--width", type=int, default=70, help="Maximum line width")
    parser.add_argument("-l", "--language", default="en_US", help="Text file locale")
    parser.add_argument("path", help="Text file path. Use '-' to read from standard input.")
    args = parser.parse_args()

    hyphenator = Hyphenator(args.language)
    if args.path == "-":
        for content in sys.stdin:
            for line in textwrap2.wrap(content, width=args.width, use_hyphenator=hyphenator):
                print(line)
    else:
        with open(args.path) as f:
            for line in textwrap2.wrap(f.read(), width=args.width, use_hyphenator=hyphenator):
                print(line)
