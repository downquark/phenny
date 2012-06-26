#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
updatedb.py - updates Commie's project database with newest torrents from nyaa, a phenny module
"""

from re import sub,match
from time import mktime,strptime,strftime
from oursql import connect
from datetime import timedelta
from feedparser import parse
from configparser import ConfigParser

def updatedb(phenny, input):
    if input.admin:
        """.updatedb - updates Commie's project database"""
        c=ConfigParser()
        c.read('updatedb.cfg')
        cfg='commie'
        d=parse(c[cfg]['url'])
        i=0
        fail=''
        command='INSERT INTO Episodes (Name,Episode,CRC,Torrent,Size) VALUES'
        conn=connect(host=c[cfg]['host'],user=c[cfg]['user'],
        passwd=c[cfg]['passwd'],db=c[cfg]['db'])
        curs=conn.cursor()
        curs.execute('SELECT Time FROM lastUpdated')
        old=curs.fetchone()[0]
        oldtime=mktime(strptime(old,'%a, %d %b %Y %H:%M:%S +0000'))
        for item in d.entries:
            t=mktime(strptime(item.published,'%a, %d %b %Y %H:%M:%S +0000'))-oldtime
            if t>1:
                m=match(r'^\[[\w|-]+\] (.+) - (\d\d[v\d]*) \[([0-9A-F]{8})\]\.mkv$',
                item.title)
                n=match(r'^.+loads - ([\d|\.]{1,6} \wiB) - .+$',item.description)
                if m==None: fail+='{} '.format(item.title)
                else:
                    i+=1
                    command+="('{}','{}','{}','{}','{}'),".format(m.group(1),
                    m.group(2),m.group(3),item.guid,n.group(1))
                    if i==1: new=item.published
            elif (i==0 and len(fail)<1) and not t>1:
                return phenny.reply('No new episodes')
            else: break
        if i>=1:
            command=sub(r',$',r';',command)
            curs.execute(command)
            curs.execute('UPDATE lastUpdated SET Time=? WHERE Time=?',(new,old))
            conn.commit()
            curs.close()
        reply='Added {} episodes succesfully'.format(i)
        if len(fail)>0: reply+=' | Please add manually: {}'.format(fail)
        return phenny.reply(reply)
updatedb.rule=(['updatedb'], r'(.*)')
updatedb.priority = 'low'

if __name__ == '__main__': 
    print(__doc__.strip())
