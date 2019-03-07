# CMPT 103 (Fall 2017)
#
# Sample code to download routes using the Open Source Routing Machine.
#
# For example, enter
#   -113.510118317736,53.54797265
# as first coordinate for MacEwan University and enter
#   -113.588802357662,53.30873035
# as the second for the Edmonton International Airport.

import http.client
import pprint

def find_route():
    start_coord = input("Enter starting coordinate (lon,lat): ")
    end_coord = input("Enter ending coordinate (lon,lat): ")

    host = "router.project-osrm.org"
    path = "/route/v1/driving/" + start_coord + ";" + end_coord
    query_string = "overview=false&geometries=polyline&steps=true"

    headers = {
        "User-Agent": "Python/3.7.2"
    }

    # create connection and send request
    connection = http.client.HTTPConnection(host)
    connection.request("GET", path + "?" + query_string, headers = headers)
    
    # obtain response and check for failure    
    response = connection.getresponse()
    if response.status != 200:
        print("request failed (" + str(response.status) + "): terminating...")
        return
    
    # read the response
    data = response.read()
    # once the response has been read, you should close the connection;
    # it's similar to files: read the file and then close it
    connection.close()

    # convert the response to a string
    string = data.decode()

    pprint.pprint(string)