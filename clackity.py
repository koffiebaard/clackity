#!/usr/bin/env python

import urllib2
import sys
import json
import MySQLdb

# Settings
fp = open('../clackity.json')
settings = json.load(fp)
print settings

# Request
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

# DB connection
db = MySQLdb.connect(host=settings["db_host"],
                         user=settings["db_username"],
                         passwd=settings["db_password"],
                         db="clackity")

def sendsClacks(url):
  cur = self.db.cursor()
  cur.execute("select * from `clacks_senders` where `url` = '%s'" % url)
  arr = cur.fetchone()
  cur.close()
  return arr

def receivedClacksFrom(self, url):

  if self.db is None:
    self.connectDB()

  cur = self.db.cursor()
  cur.execute("""
	insert into `clacks_senders` (`url`) values ('%s')
  """, (url,))
  self.db.commit()
  cur.close()


if len(sys.argv) > 1:
    url = sys.argv[1]
    
    response = urllib2.urlopen(HeadRequest(url))

    for header in response.headers:
        if header == "x-clacks-overhead":
            receivedClacksFrom(url)
            print "yarr!"
