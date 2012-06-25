#!/usr/bin/python3
"""
linx.py - linx.li tools
author: mutantmonkey <mutantmonkey@mutantmonkey.in>, andreim <andreim@andreim.net>
"""

from urllib.error import HTTPError
from tools import GrumbleError
import web
import json


def linx(phenny, input):
    """.linx <url> - Upload a URL to linx.li."""

    url = input.group(2)
    if not url:
        phenny.reply("No URL provided. CAN I HAS?")
        return

    try:
        req = web.post("http://linx.li/vtluug", {'url': url})
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    data = json.loads(req)
    if len(data) <= 0 or not data['success']:
        phenny.reply('Sorry, upload failed.')
        return

    phenny.reply(data['url'])
linx.rule = (['linx'], r'(.*)')


def lines(phenny, input):
    """.lines <nickname> (<today/yesterday/YYYYMMDD>) - Returns the number of lines a user posted on a specific date."""

    if input.group(2):
        info = input.group(2).split(" ")

        if len(info) == 1:
            nickname = info[0]
            date = "today"
        elif len(info) == 2:
            nickname = info[0]
            date = info[1]
        else:
            phenny.reply(".lines <nickname> (<today/yesterday/YYYYMMDD>) - Returns the number of lines a user posted on a specific date.")
            return

    else:
        nickname = input.nick
        date = "today"

    try:
        req = web.post("http://linx.li/vtluuglines", {'nickname': nickname, 'date': date, 'sender': input.nick})
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    phenny.reply(req)

lines.rule = (['lines'], r'(.*)')


def posted(phenny, input):
    """.posted <message> - Checks if <message> has already been posted."""

    message = input.group(2)
    if not message:
        phenny.say(".posted <message> - Checks if <message> has already been posted.")
        return

    try:
        req = web.post("http://linx.li/vtluugposted", {'message': message, 'sender': input.nick})
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    phenny.reply(req)

posted.rule = (['posted'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())