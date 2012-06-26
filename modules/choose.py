#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
choose.py - sometimes you just can't decide, a phenny module
"""

import re, random

def c(phenny, input):
    """.c <red> <blue> - for when you just can't decide"""
    origterm = input.groups()[1]
    if not origterm:
        return phenny.say(".c <red> <blue> - for when you just can't decide")
    choose = re.findall(r'([^,]+)', origterm)
    if len(choose) == 1:
        choose = re.findall(r'(\S+)', origterm)
        if len(choose) == 1:
            return phenny.reply("%s" % (choose[0].strip()))
    fate = random.choice(choose).strip()
    return phenny.reply("%s" % (fate))
c.rule = (['c'], r'(.*)')

if __name__ == '__main__': 
    print(__doc__.strip())
