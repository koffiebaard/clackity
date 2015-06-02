#!/usr/bin/env python

import urllib2
import sys

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


if len(sys.argv) > 1:
    url = sys.argv[1]
    
    response = urllib2.urlopen(HeadRequest(url))

    for header in response.headers:
        if header == "x-clacks-overhead":
            print "yarr"
