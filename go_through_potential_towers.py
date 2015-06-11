#!/usr/bin/env python

import urllib2
import sys
import json
import MySQLdb
from datetime import datetime
from urlparse import urlparse
from subprocess import call

# Settings
fp = open('/web/clackity.json')
settings = json.load(fp)

# DB connection
db = MySQLdb.connect(host=settings["db_host"],
                         user=settings["db_username"],
                         passwd=settings["db_password"],
                         db="clackity")

def getTowers():
  cur = db.cursor()
  cur.execute("select * from `potential_towers` order by `added` asc limit 100")
  arr = cur.fetchall()
  cur.close()
  return arr

def towerChecked(domainname):
  cur = db.cursor()
  cur.execute("""
	delete from `potential_towers` where `domainname` = %s
  """, (domainname,))
  db.commit()
  cur.close()


towers = getTowers()

if towers:
    for tower in towers:
        if tower[0] is not None:
            call("/web/clackity/check_signal.py " + tower[0], shell=True)
            towerChecked(tower[0])
