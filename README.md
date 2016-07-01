# Pairwise

Designed for Rands' Slack channel #chatroulette.  Builds the pairs, and
checks the history to see if any pairs have been seen before (inside the
relevant-history value).  

Also featured, coworkers can be built in a different JSON doc, and coworkers
won't be matched together.

## Document formats:
### pairwise_names.json
JSON list of all participants in chat roulette

### pairwise_coworkers.json
JSON list of lists.  Each set of coworkers is a list.

### pairwise_history.json
JSON Dictionary.  The key is the date/time stamp of each pair set building.
The values are lists of pair lists.

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
