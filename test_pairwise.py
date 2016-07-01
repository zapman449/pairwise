#!/usr/bin/env python

from __future__ import print_function, division, absolute_import
import pairwise


def test_makepairs1():
    names = ['aaa', 'bbb', 'ccc', 'ddd']
    pairs = pairwise.make_pairs(names)
    assert len(pairs) == 2


def test_makepairs2():
    names = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
    pairs = pairwise.make_pairs(names)
    assert len(pairs) == 2
    assert len(pairs[0]) + len(pairs[1]) == 5


def test_validatepairs1():
    pairs = []
    pairs.append(set(['aaa', 'bbb']))
    pairs.append(set(['ccc', 'ddd']))
    historical_pairs = []
    historical_pairs.append(set(['aaa', 'bbb']))
    assert pairwise.validate_pairs(pairs, historical_pairs) is False


def test_validatepairs2():
    pairs = []
    pairs.append(set(['aaa', 'bbb']))
    pairs.append(set(['ccc', 'ddd']))
    historical_pairs = []
    historical_pairs.append(set(['aaa', 'ccc']))
    assert pairwise.validate_pairs(pairs, historical_pairs) is True


def test_relevanthistory1():
    metahistory = {
        "2016-07-01 16:25:54.376811": [['aaa', 'bbb'], ['ccc', 'ddd']],
        "2016-07-01 16:26:22.020641": [['fff', 'ggg'], ['hhh', 'iii']],
        "2016-07-01 16:27:47.599132": [['jjj', 'kkk'], ['lll', 'mmm']],
        "2016-07-01 16:48:04.645997": [['nnn', 'ooo'], ['ppp', 'qqq', 'rrr']],
        "2016-07-01 16:48:46.545811": [['sss', 'ttt'], ['uuu', 'vvv']]
    }
    result = pairwise.prune_history(metahistory, 2)
    assert len(result) == 4
    assert len(result[1]) == 3
