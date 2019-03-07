# CMPT 103 (Fall 2017)
#
# Sample code to download Schedule Photo Enforcement data from the
# City of Edmonton.

import http.client
import pprint
import json

def get_json():
    # http://data.edmonton.ca/api/views/4cqz-cd52/rows.json?accessType=DOWNLOAD
    host = "data.edmonton.ca"
    path = "/api/views/4cqz-cd52/rows.json"
    queryString = "accessType=DOWNLOAD"    
    
    # create connection and send request
    connection = http.client.HTTPConnection(host)
    connection.request("GET", path + "?" + queryString)
    
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
    
    new_file = open('enforcement_coe.json', 'w')
    new_file.write(string)
    
    #pprint.pprint(string)