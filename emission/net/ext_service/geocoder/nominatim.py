from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import logging
import json

from emission.core.wrapper.trip_old import Coordinate
from pygeocoder import Geocoder as pyGeo  ## We fall back on this if we have to

try:
    googlemaps_key_file = open("conf/net/ext_service/googlemaps.json")
    GOOGLE_MAPS_KEY = json.load(googlemaps_key_file)["api_key"]
except:
    print("google maps key not configured, falling back to nominatim")

try:
    nominatim_file = open("conf/net/ext_service/nominatim.json")
    NOMINATIM_QUERY_URL = json.load(nominatim_file)["query_url"]
except:
    print("nominatim not configured either, place decoding must happen on the client")

used_nominatim_already = False

class Geocoder(object):

    def __init__(self):
        pass

    @classmethod
    def make_url_geo(cls, address):
        params = {
            "q" : address,
            "format" : "json"
        }

        query_url = NOMINATIM_QUERY_URL + "/search?"
        encoded_params = urllib.parse.urlencode(params)
        url = query_url + encoded_params
        logging.debug("For geocoding, using URL %s" % url)
        return url

    @classmethod
    def get_json_geo(cls, address):
        global used_nominatim_already
        if used_nominatim_already:
            print("TIAGO: nominatim.py:get_json_geo used nominatim already, skipping")
            return
        else:
            print("TIAGO: nominatim.py:get_json_geo first use of nominatim")
            used_nominatim_already = True
        request = urllib.request.Request(cls.make_url_geo(address))
        response = urllib.request.urlopen(request)
        jsn = json.loads(response.read())
        return jsn

    @classmethod
    def geocode(cls, address):
        # try:
        #     jsn = cls.get_json_geo(address)
        #     lat = float(jsn[0]["lat"])
        #     lon = float(jsn[0]["lon"])
        #     return Coordinate(lat, lon)
        # except:
        #     print "defaulting"
        return _do_google_geo(address) # If we fail ask the gods


    @classmethod
    def make_url_reverse(cls, lat, lon):
        params = {
            "lat" : lat,
            "lon" : lon,
            "format" : "json"
        }
        print("TIAGO: nominatim.py:make_url_reverse start")
        query_url = NOMINATIM_QUERY_URL + "/reverse?"
        print("TIAGO: nominatim.py:make_url_reverse query_url %s" % query_url)
        encoded_params = urllib.parse.urlencode(params)
        url = query_url + encoded_params
        print("For reverse geocoding, using URL %s" % url)
        return url

    @classmethod
    def get_json_reverse(cls, lat, lng):
        parsed_response = json.loads('{"place_id":137488079,"licence":"Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright","osm_type":"way","osm_id":257530977,"lat":"37.38825945","lon":"-122.087611868098","display_name":"775, South Shoreline Boulevard, Mountain View, Santa Clara County, Kalifornien, 94040, Vereinigte Staaten von Amerika","address":{"house_number":"775","road":"South Shoreline Boulevard","city":"Mountain View","county":"Santa Clara County","state":"Kalifornien","postcode":"94040","country":"Vereinigte Staaten von Amerika","country_code":"us"},"boundingbox":["37.3881323","37.3883631","-122.087766","-122.0873533"]}')
        #logging.debug("parsed_response = %s" % parsed_response)
        #print("parsed_response = %s" % parsed_response)
        return parsed_response

        # global used_nominatim_already
        # logging.debug("TIAGO: nominatim.py:get_json_reverse start")
        # #print("TIAGO: nominatim.py:get_json_reverse start... used_nominatim_already %s" % used_nominatim_already)
        # if used_nominatim_already == True:
        #     used_nominatim_already = True
        #     print("TIAGO: nominatim.py:get_json_reverse used nominatim already, skipping")
        #     return
        # else:
        #     used_nominatim_already = True
        #     print("TIAGO: nominatim.py:get_json_reverse first use of nominatim")
        # print("TIAGO: nominatim.py:get_json_reverse getting request")
        # request = urllib.request.Request(cls.make_url_reverse(lat, lng))
        # print("TIAGO: nominatim.py:get_json_reverse getting response")
        # response = urllib.request.urlopen(request)
        # print("TIAGO: nominatim.py:get_json_reverse parsing response")
        # parsed_response = json.loads(response.read())
        # #logging.debug("parsed_response = %s" % parsed_response)
        # print("parsed_response = %s" % parsed_response)
        # return parsed_response

    @classmethod
    def reverse_geocode(cls, lat, lng):
        # try:
        #     jsn = cls.get_json_reverse(lat, lng)
        #     address = jsn["display_name"]
        #     return address

        # except:
        #     print "defaulting"
        return _do_google_reverse(lat, lng) # Just in case

## Failsafe section
def _do_google_geo(address):
    geo = pyGeo(GOOGLE_MAPS_KEY)
    results = geo.geocode(address)
    return Coordinate(results[0].coordinates[0], results[0].coordinates[1])

def _do_google_reverse(lat, lng):
    geo = pyGeo(GOOGLE_MAPS_KEY)
    address = geo.reverse_geocode(lat, lng)
    return address[0]
