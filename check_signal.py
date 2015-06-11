#!/usr/bin/env python

import urllib2
import sys
import json
import MySQLdb
from datetime import datetime
from urlparse import urlparse

# Settings
fp = open('/web/clackity.json')
settings = json.load(fp)

# Request
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

# DB connection
db = MySQLdb.connect(host=settings["db_host"],
                         user=settings["db_username"],
                         passwd=settings["db_password"],
                         db="clackity")

def urlToDomainname(url):
  parsed_uri = urlparse(url)
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
  return domain


def sendsClacks(url):
  domain = urlToDomainname(url)
  cur = db.cursor()
  cur.execute("select * from `clacks_senders` where `domainname` = '%s'" % domain)
  arr = cur.fetchone()
  cur.close()
  return arr

def isALittleBitch(url):
  domain = urlToDomainname(url)
  cur = db.cursor()
  cur.execute("select * from `bitches` where `domainname` = '%s'" % domain)
  arr = cur.fetchone()
  cur.close()
  return arr

def littleBitchAcknowledgement(url):
  domain = urlToDomainname(url)
  cur = db.cursor()
  cur.execute("""
	insert into `bitches` (`domainname`, `last_checked`) values (%s, %s)
  """, (domain,datetime.now()))
  db.commit()
  cur.close()


def receivedClacksFrom(url):
  domain = urlToDomainname(url)
  cur = db.cursor()
  cur.execute("""
	insert into `clacks_senders` (`domainname`, `added`) values (%s, %s)
  """, (domain,datetime.now()))
  db.commit()
  cur.close()



def checkURL(url):
    if sendsClacks(url) is None and isALittleBitch(url) is None:    
      response = urllib2.urlopen(HeadRequest(url))

      for header in response.headers:
          if header == "x-clacks-overhead":
              receivedClacksFrom(url)
              print "yarr!"
              return True
      
      littleBitchAcknowledgement(url)
      return False


if len(sys.argv) > 1:
    url = sys.argv[1]
    checkURL(url)


