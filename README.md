# Pairwise

Designed for Rands' Slack channel #face-to-face.  Builds the pairs, and
checks the history to see if any pairs have been seen before (inside the
relevant-history value).  

Also featured, coworkers can be built in a different JSON doc, and coworkers
won't be matched together.

## Document formats:
### pairwise_names.json
JSON list of all participants in face-to-face conversations

### pairwise_coworkers.json
JSON list of lists.  Each set of coworkers is a list.

### pairwise_history.json
JSON Dictionary.  The key is the date/time stamp of each pair set building.
The values are lists of pair lists.

### slack_creds.json
JSON Dictionary.  The following three keys and values need to be set:
1. 'slack_api_token'.  Value is your slack_api_token
2. 'user'.  The value is your username in the slack
3. 'channel'.  The value is the name of the channel where the 'all pairings' message would go

And the following two keys are optional:
1. 'dm_template_two': python template string for the DMs for pairings of two people.  Needs to specify {0}, {1}, and {2} for recipient, partner, and source user (aka you)

   * example:
       ```
       "dm_template_two": "Hey @{0}! you've been paired with @{1} in #face-to-face.  Please setup a meeting when you can.  If you have any questions, concerns or issues, please contact @{2}",
       ```

2. 'dm_template_three': python template string for the DMs for pairings of three people.  Needs to specify {0}, {1}, {2} and {3} for recipient, partner1, partner2, and source user (aka you)

   * example:
       ```
       "dm_template_three": "Hey @{0}! you've been paired with @{1} and @{2} in #face-to-face.  Please setup a meeting when you can.  If you have any questions, concerns or issues, please contact @{3}"
       ```


## Usage:

```
$ ./pairwise.py
```

Will build a pairing set.  By default 8 past pairings are considered relevant.
The three files can be overridden by command line arguments.

## Syntax:

```
./pairwise.py -h
usage: pairwise.py [-h] [--history HISTORY] [--coworkers COWORKERS]
                   [--names NAMES] [--relevant-history RELEVANT_HISTORY]

optional arguments:
  -h, --help            show this help message and exit
  --history HISTORY     File for pair history
  --coworkers COWORKERS
                        File for lists of coworkers
  --names NAMES         File for the list participant names
  --relevant-history RELEVANT_HISTORY
                        Number of past pairings to consider when validating
                        pairs
```

### pairwise-add-member.py
```
$ ./pairwise-add-member.py <member>
```

Adds member to the list of names

### pairwise-remove-member.py
```
pairwise-remove-member.py <member>
```

Removes member from the list of names

### pairwise-post-recent-pairings.py
```
pairwise-post-recent-pairings.py [-d]
```

Posts the most recent pairings to slack.  A DM to each user with their partner, and one message to the CHANNEL specified in slack_creds.json with all pairings.
