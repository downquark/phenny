#!/usr/bin/env python
# coding=utf-8
"""
calc.py - Phenny Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web

r_result = re.compile(r'(?i)<A NAME=results>(.*?)</A>')
r_tag = re.compile(r'<\S+.*?>')

subs = [
    (' in ', ' -> '), 
    (' over ', ' / '), 
    ('£', 'GBP '), 
    ('€', 'EUR '), 
    ('\$', 'USD '), 
    (r'\bKB\b', 'kilobytes'), 
    (r'\bMB\b', 'megabytes'), 
    (r'\bGB\b', 'kilobytes'), 
    ('kbps', '(kilobits / second)'), 
    ('mbps', '(megabits / second)')
]

def c(phenny, input): 
    """Google calculator."""
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    q = input.group(2)
    q = q.replace('\xcf\x95', 'phi') # utf-8 U+03D5
    q = q.replace('\xcf\x80', 'pi') # utf-8 U+03C0
    uri = 'http://www.google.com/ig/calculator?q='
    bytes = web.get(uri + web.quote(q))
    parts = bytes.split('",')
    answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
    if answer: 
        #answer = ''.join(chr(ord(c)) for c in answer)
        #answer = answer.decode('utf-8')
        answer = answer.replace('\\x26#215;', '*')
        answer = answer.replace('\\x3c', '<')
        answer = answer.replace('\\x3e', '>')
        answer = answer.replace('<sup>', '^(')
        answer = answer.replace('</sup>', ')')
        answer = web.decode(answer)
        phenny.say(answer)
    else: phenny.reply('Sorry, no result.')
c.commands = ['c']
c.example = '.c 5 + 3'

def py(phenny, input): 
    query = input.group(2) or ""
    uri = 'http://tumbolia.appspot.com/py/'
    answer = web.get(uri + web.quote(query))
    if answer: 
        phenny.say(answer)
    else: phenny.reply('Sorry, no result.')
py.commands = ['py']

def wa(phenny, input): 
    if not input.group(2):
        return phenny.reply("No search term.")
    query = input.group(2)
    uri = 'http://tumbolia.appspot.com/wa/'

    answer = web.get(uri + web.quote(query.replace('+', '%2B')))
    try:
        answer = answer.split(';')[1]
    except IndexError:
        answer = ""

    if answer: 
        phenny.say(answer)
    else: phenny.reply('Sorry, no result.')
wa.commands = ['wa']

if __name__ == '__main__': 
    print(__doc__.strip())
