#!/usr/bin/env python

# from __future__ import print_function, division, absolute_import, unicode_literals
from __future__ import print_function, division, absolute_import
import argparse
import json
# import os.path
# import sys

import slacker

HISTORY = "./pairwise_history.json"
CREDS = "./slack_creds.json"


def parse_cli(test_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dry-run", dest="dry_run", action='store_true',
                        help="dry run everything")
    if test_args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(test_args)
    return args


def slack_login():
    global CREDS
    with open(CREDS, 'r') as f:
        jdict = json.load(f)
    slack_api_token = jdict['slack_api_token']
    slack = slacker.Slacker(slack_api_token)
    return slack, jdict['user'], jdict['channel']


def get_most_recent_pairs(args):
    global HISTORY
    with open(HISTORY, 'r') as f:
        history = json.load(f)
    latest_key = sorted(history.keys())[-1]
    return history[latest_key]


def send_message_pairings(pair, args):
    if len(pair) == 2:
        message0 = "Hey @{0}! you've been paired with @{1} in #chatroulette.  Please setup a meeting when you can.".format(pair[0], pair[1])
        message1 = "Hey @{0}! you've been paired with @{1} in #chatroulette.  Please setup a meeting when you can.".format(pair[1], pair[0])
    elif len(pair) == 3:
        message0 = "Hey @{0}! you've been paired with @{1} and @{2} in #chatroulette.  Please setup a meeting when you can.".format(pair[0], pair[1], pair[2])
        message1 = "Hey @{0}! you've been paired with @{1} and @{2} in #chatroulette.  Please setup a meeting when you can.".format(pair[1], pair[0], pair[2])
        message2 = "Hey @{0}! you've been paired with @{1} and @{2} in #chatroulette.  Please setup a meeting when you can.".format(pair[2], pair[0], pair[1])
    if args.dry_run is True:
        print("This message would be sent to {0}:".format(pair[0]))
        print(message0)
        print("This message would be sent to {0}:".format(pair[1]))
        print(message1)
        if len(pair) == 3:
            print("This message would be sent to {0}".format(pair[2]))
            print(message2)
        print()
    else:
        args.slack.chat.post_message("@" + pair[0], message0, username=args.user)
        args.slack.chat.post_message("@" + pair[1], message1, username=args.user)
        if len(pair) == 3:
            args.slack.chat.post_message("@" + pair[2], message2)


def send_all_pairings(pairs, args):
    message = ""
    counter = 0
    for pair in pairs:
        counter += 1
        if len(pair) == 2:
            message += "Pair {0:02d}: {1} and {2}\n".format(counter, pair[0], pair[1])
        elif len(pair) == 3:
            message += "Pair {0:02d}: {1}, {2} and {3}\n".format(counter, pair[0], pair[1], pair[2])
    if args.dry_run is True:
        print("would send this message to {0}".format(args.channel))
        print(message)
    else:
        args.slack.chat.post_message(args.channel, message, username=args.user)


def main():
    args = parse_cli()
    args.slack, args.user, args.channel = slack_login()
    pairs = get_most_recent_pairs(args)
    # testing override
    pairs = [["jimkogs", "michaelhoney", "royrapoport"]]
    for pair in pairs:
        send_message_pairings(pair, args)
    send_all_pairings(pairs, args)


if __name__ == "__main__":
    main()
