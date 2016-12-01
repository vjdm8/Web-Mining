# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 10:31:19 2016

@author: Vivek Martins

Code to return  Place_ID from google map api
can be uncommented to obtain latitude and longitude
"""

import urllib
import json

# serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
serviceurl = 'http://python-data.dr-chuck.net/geojson?'

while True:
    address = raw_input('Enter location: ')
    if len(address) < 1 : break

    url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
    print 'Retrieving', url
    uh = urllib.urlopen(url)
    data = uh.read()
    print 'Retrieved',len(data),'characters'


    try: js = json.loads(str(data))
    except: js = None
    if 'status' not in js or js['status'] != 'OK':
        print '==== Failure To Retrieve ===='
        print data
        continue
    """#Uncomment to look at JSON architecture
    print json.dumps(js, indent=4)"""
    PID = js["results"][0]["place_id"]
    """
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    
    """
    print 'Place_ID',PID
    
    #location = js['results'][0]['formatted_address']
    #print location
