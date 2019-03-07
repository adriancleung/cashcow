# CMPT 103 (Fall 2017)
#
# Sample code to download location data for a search string using
# openstreetmap.org.

import http.client
import urllib.parse
import pprint
import json
import pickle

def find_location():
    search_terms = input("Enter search terms: ")
    
    # using the quote function, make the user's search terms "safe" for
    # inclusion in the path
    search_terms = urllib.parse.quote(search_terms)
    
    host = "nominatim.openstreetmap.org"
    path = "/search/" + search_terms
    query_string = "format=json"
    
    # searches of openstreetmap.org require that you tell them about your
    # web browser; let's tell them that we're using Python!
    headers = {
        "User-Agent": "Python/3.7.2"
    }

    # create connection and send request
    connection = http.client.HTTPConnection(host)
    connection.request("GET", path + "?" + query_string, headers=headers)
    
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
    string = string.replace('©', '')
    string.rstrip(']')
    string.lstrip('[')
    
    new_file = open('search_results.json', 'w')
    new_file.write(string)
    new_file = open('search_results.json', 'r')
    #for key in new_file:
    #    print(key)
    #pickle.dump(string, new_file)
    
    #for key in new_file:
    #    print(key)
    
    pprint.pprint(string)