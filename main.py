"""
Harrison Hall

Main file for running the game. 
"""

import argparse as ap
from sys import exit

from implib import Basic
from implib import CurHandler


all_games = [
    "demo",
    "main"
]


def setup_parser() -> ap.ArgumentParser:
    global all_games
    
    parser = ap.ArgumentParser(
        description="CLI Game by Harrison Hall"
    )
    parser.add_argument(
        "-B", "-b", "--basic",
        action="store_true",
        help="run basic CLI game"
    )
    parser.add_argument(
        "-C", "-c", "--curses",
        action="store_true",
        help="run curses game"
    )
    parser.add_argument(
        "-G", "-g", "--game",
        action="store",
        default="demo",
        help=f"select game from {all_games}"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = setup_parser()

    if args.game not in all_games:
        exit(f"Invalid game, try from {all_games}")

    if args.basic and not args.curses:
        Basic.main(*Basic.setup())
        exit()

    if args.curses and not args.basic:
        CurHandler.main(*CurHandler.setup())
        exit()

    if not args.curses and not args.basic:
        CurHandler.main(*CurHandler.setup())
        exit()

    exit("Options not valid. Try with -h.")
