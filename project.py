# Adrian Leung
# Cash Cow Project
# project.py
# adrian.leung@ualberta.ca

import os
import json
import pprint
import math

from get_route import *
from get_place_coords import *
from get_enforcement import *
from graphics import *


def main():
    # Purpose: The main function that calls the menu
    # Parameters: Takes no parameters
    # Return: None 
    
    menu()

def menu():
    # Purpose: Prints out the menu for the Cash Cow Explorer Program
    # Parameters: Takes no parameters
    # Return: None
    
    #lst = []
    #locations = {}
    route_data = []
    enforcement_data = {}
    nearby = []
    
    while True: 
        print('''
=== Cash Cow Explorer ===
(1) Load route data from file
(1.1) Find location coordinates (not implemented)
(1.2) Load route from coordinates (not implemented)
(2) Interpolate route data
(3) Print route data
(4) Print summary of route data
    
(5) Load enforcement data from file
(5.1) Load enforcement data from the City of Edmonton
(6) Print enforcement data
(7) Print summary of enforcement data
        
(8) Print nearby enforcement
(9) Display data graphically
        
(0) Quit
''')
        
        user_input = input('Enter command: ')
        option_lst = ['1', '1.1', '1.2',  '2', '3', '4', '5', '5.1',  '6', '7', '8', '9', '0']
        
        if user_input not in option_lst:
            print('\nInvalid command. Please enter again')
            #continue
        else:
            if user_input == '1':
                route_data = [] # resets list to empty
                load_route_data(route_data)
            if user_input == '1.1':
                continue
                find_coords()
            if user_input == '1.2':
                continue
                route_data = []
                load_route_data_from_coords(route_data)
            if user_input == '2':
                interpolate_route_data(route_data)
            if user_input == '3':
                print_route_data(route_data)
            if user_input == '4':
                print_summary_of_route_data(route_data)
            if user_input == '5':
                enforcement_data = {} # resets the dictionary to empty
                load_enforcement_data(enforcement_data)
            if user_input == '5.1':
                enforcement_data = {}
                load_enforcement_data_from_CoE(enforcement_data)
            if user_input == '6':
                print_enforcement_data(enforcement_data)
            if user_input == '7':
                print_summary_of_enforcement_data(enforcement_data)
            if user_input == '8':
                nearby = []
                print_nearby_enforcement(route_data, enforcement_data, nearby)
            if user_input == '9':
                display_data_graphically(route_data, enforcement_data, nearby)
            if user_input == '0':
                break

def load_route_data(route_data):
    # Purpose: Loads the json data from a file that the user
    # inputted. If no data inputted, open default data.
    # Parameters: Takes the list from the menu function
    # Return: The same list with appended objects
    
    filename = str(input('\nEnter file name [route.json]: '))
    
    if os.path.isfile(filename): # checks if filename is a real file
        open_file = open(filename, 'r')
        python_data = open_file.read()
        data = json.loads(python_data)
        open_file.close()
        
        for obj in data['routes'][0]['legs'][0]['steps']:
            for loc in obj['intersections']:
                route_data.append((loc['location'][0],
                            loc['location'][1]))
                # appends lat and long to the list in tuple form
        
        return route_data
    
    elif filename == '': # opens default file if no file stated
        open_file = open('route.json', 'r')
        python_data = open_file.read()
        data = json.loads(python_data)
        open_file.close()
        
        for obj in data['routes'][0]['legs'][0]['steps']:
            for loc in obj['intersections']:
                route_data.append((loc['location'][0],
                            loc['location'][1]))
                # appends lat and long to the list in tuple form

        return route_data
    
    else: # if cannot find file
        print('\nError: cannot open file')
        load_route_data(route_data)
        
def interpolate_route_data(route_data):
    # Purpose:
    # Parameters:
    # Return:
    
    threshold = input('\nEnter threshold [100 m]: ')
    distance = 0
    counter = 0
    
    if threshold == '':
        threshold = '100'
    
    while counter != len(route_data):
        #if counter == len(route_data):
        #    break
        #else:
        counter = len(route_data)
        for i in range(len(route_data) - 1):
            distance = metres_between(route_data[i], route_data[i+1])
            distance_long = (route_data[i][0] + route_data[i+1][0]) / 2
            distance_lat = (route_data[i][1] + route_data[i+1][1]) / 2
            if distance > float(threshold):
                route_data.insert(i + 1, (distance_long, distance_lat))
         #   continue
    return(route_data)    

def print_route_data(route_data):
    # Purpose: Print the intersection locations from the user's data.
    # If no data is available, it displays 'NO POINTS LOADED'
    # Parameters: Takes the list from menu function
    # Return: None
    
    print('\nRoute Data:')
    
    if route_data == []:
        print('  NO POINTS LOADED')
    else:
        for intersections in route_data:
            print('  ' + '({:.5f}, {:0.5f})'.format(intersections[0], 
                                                    intersections[1]))
            # formats the points to 5 decimal places and adds brackets
    
def print_summary_of_route_data(route_data):
    # Purpose: Prints the number of points on the route, the total distance,
    # the average segment between each point, and the maximum segment
    # Parameters: Takes the list from the menu function
    # Return: None
    
    print('\nSummary of Route Data:\n  Points:          ''', end = '')
    total_distance = 0
    counter = 0
    tmp = 0
    
    for elem in route_data:
        counter+= 1
        
    if counter == 0:
        print('0\n  Total distance:  N/A\n  Average segment: N/A\n' + 
              '  Maximum segment: N/A')
    else:
        print(counter)
        for i in range(len(route_data)):
            if i == (len(route_data) - 1):
                print('  Total distance:  ' + '{:.5f}'.format(total_distance) + 
                      '\n  Average segment: ' + '{:.5f}'.format(average_segment)
                      + '\n  Maximum segment: ' + '{:.5f}'.format(tmp))
            else:
                total_distance += metres_between(route_data[i], 
                                                 route_data[i + 1])
                average_segment = total_distance / (counter-1)
                if metres_between(route_data[i], route_data[i + 1]) > tmp:
                    tmp = metres_between(route_data[i], route_data[i + 1])
    
# metres_between calculates and returns the metres between point_a and
# point_b where each point is a 2-element list [longitude, latitude]
# or a 2-tuple (longitude, latitude).
#
# Adapted from https://rosettacode.org/wiki/Haversine_formula#Python
def metres_between(point_a, point_b):
    R = 6372.8 # Earth radius in kilometers

    delta_lat = math.radians(point_b[1] - point_a[1])
    delta_lon = math.radians(point_b[0] - point_a[0])
    point_a1 = math.radians(point_a[1])
    point_b1 = math.radians(point_b[1])
   
    a = (math.sin(delta_lat/2)**2 +
         math.cos(point_a1) * math.cos(point_b1) * math.sin(delta_lon/2)**2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c * 1000.0

def load_enforcement_data(enforcement_data):
    # Purpose: Loads the enforcement data from file
    # Parameters: Takes the dicationary from the menu function
    # Return: The dictionary with added keys and values
    
    filename = str(input('\nEnter file name [enforcement.json]: '))
    
    if os.path.isfile(filename): # checks if filename is a real file
        open_file = open(filename, 'r')
        python_data = open_file.read()
        data = json.loads(python_data)
        open_file.close()
        
        for value in data['data']:
            enforcement_data[(value[16], value[15])] = value[10]
            # adds key (lat, long) with value of street name

        return enforcement_data
    
    elif filename == '': # opens default file if no file stated
        open_file = open('enforcement.json', 'r')
        python_data = open_file.read()
        data = json.loads(python_data)
        open_file.close()
        
        for value in data['data']:
            enforcement_data[(value[16], value[15])] = value[10]
            # adds key (lat, long) with value of street name

        return enforcement_data
    
    else: # if cannot find file
        print('\nError: cannot open file')
        load_enforcement_data(enforcement_data)    

def load_enforcement_data_from_CoE(enforcement_data):
    get_json()
    try:
        open_file = open('enforcement_coe.json', 'r')
        python_data = open_file.read()
        data = json.loads(python_data)
        open_file.close()
        
        for value in data['data']:
            enforcement_data[(value[16], value[15])] = value[10]
        
        print('\nEnforcement Data loaded from City of Edmonton')
        
        return enforcement_data
    
    except:
        print('\nCannot load enforcement data from City of Edmonton')

def print_enforcement_data(enforcement_data):
    # Purpose: Prints the locations of the camera with street names
    # Parameters: Takes the dictionary from the menu function
    # Return: None
    
    print('\nEnforcement Data:')
    
    if enforcement_data == {}:
        print('  NO POINTS LOADED')
    else:
        for points in enforcement_data:
            print('  ' + '({:.5f}, {:.5f})'.format(float(points[0]), 
                                                   float(points[1])) + ' -- ' + 
                  enforcement_data[points])

def print_summary_of_enforcement_data(enforcement_data):
    # Purpose: Prints the summary of the travel directions where the camera
    # is pointing
    # Parameters: Takes the dictionary from the menu function
    # Return: None
    
    north_counter = 0
    south_counter = 0
    east_counter = 0
    west_counter = 0
    
    for points in enforcement_data:
        if enforcement_data[points][0] == 'N':
            north_counter += 1
        elif enforcement_data[points][0] == 'S':
            south_counter += 1
        elif enforcement_data[points][0] == 'E':
            east_counter += 1
        elif enforcement_data[points][0] == 'W':
            west_counter += 1    
    
    print('\nSummary of Enforcement Data:\n' + '  Northbound:  ' +
          str(north_counter) + '\n  Eastbound:   ' + str(east_counter) + 
          '\n  Southbound:  ' + str(south_counter) + 
          '\n  Westbound:   ' + str(west_counter))
    
    
def print_nearby_enforcement(route_data, enforcement_data, nearby):
    # Purpose:
    # Parameters:
    # Return:    
    
    load_nearby(route_data, enforcement_data, nearby)
    
    print('\nNearby Enforcement Locations:')
    #for points in route_data:
    #   for loc in enforcement_data:
    #        distance = metres_between(points, (float(loc[0]), float(loc[1])))
    #        if distance <= 100 and loc not in nearby:
    #            nearby.append(loc)
    for loc in nearby:
        print('  ' + '({:.5f}, {:.5f})'.format(float(loc[0]), 
                                                   float(loc[1])) + ' -- ' + 
                  enforcement_data[loc])
        
    #return nearby

def load_nearby(route_data, enforcement_data, nearby):
    for points in route_data:
        for loc in enforcement_data:
            distance = metres_between(points, (float(loc[0]), float(loc[1])))
            if distance <= 100 and loc not in nearby:
                nearby.append(loc)
                
    return nearby

def display_data_graphically(route_data, enforcement_data, nearby):
    # Purpose: Shows a map in a gpraphical window
    # Parameters: Takes the route_data, enforcement_data, and nearby_data
    # Return: None
    
    route_counter = True
    enforcement_counter = True
    nearby_counter = True
    route_lst = []
    enforcement_lst = []
    nearby_lst = []
    point_lst = []
    
    win = GraphWin('Cash Cow', 750, 768)
    win.setCoords(-113.71360, 53.39595, -113.28323, 53.65785)
    background = Image(Point(-113.498415, 53.5269), 'background.gif')
    background.draw(win)
    text = '(r) toggle route; (n) toggle near; (o) toggle other; (q) quit'
    instructions = Text(Point(-113.498415, 53.401), text)
    instructions.setSize(20)
    instructions.setStyle('bold')
    instructions.draw(win)
    while True:
        try:
            user_input = win.getKey()
            if user_input == 'r':
                route_counter, route_lst = toggle_route(route_data, 
                                                route_counter, route_lst, win)
            if user_input == 'n':
                nearby_counter, nearby_lst = toggle_nearby(nearby, nearby_lst, 
                                                    nearby_counter, win)
            if user_input == 'o':
                enforcement_counter, enforcement_lst = toggle_other(
                    enforcement_data, enforcement_lst, enforcement_counter, 
                    nearby, win)
            if user_input == 'q':
                win.close()
                break
        except:
            break
        
    win.close()
        
def toggle_route(route_data, route_counter, route_lst, win):
    # Purpose: Show/hide the route on the graphical window
    # Parameters: Takes the route_data list, bool route_couter, route_lst list,
    # and the graphical window win.
    # Return: True or false route_counter and route_lst with the route points
    
    if route_counter:
        for i in range(len(route_data) - 1):
            p1 = Point(route_data[i][0], route_data[i][1])
            p2 = Point(route_data[i+1][0], route_data[i+1][1])
            route = Line(p1, p2)
            route_lst.insert(0, route)
            route.setWidth(2)
            route.draw(win)
            
        route_counter = False
    else:
        for line in route_lst:
            line.undraw()
            
        route_lst = []
        route_counter = True
        
    return route_counter, route_lst
        
def toggle_nearby(nearby, nearby_lst, nearby_counter, win):
    # Purpose: Show/hide the nearby camera location in the graphical window
    # Parameters: Takes the nearby dat, nearby_lst points, bool nearby_counter,
    # and the graphical window win
    # Return: True or fale nearby_counter and the nearby_lst points
    
    if nearby_counter:
        for loc in nearby:
            point = Point(float(loc[0]), float(loc[1]))
            dollar_nearby = Image(point, 'dollar_nearby.gif')
            nearby_lst.append(dollar_nearby)
            nearby_lst.append(point)
            dollar_nearby.draw(win)
            point.draw(win)
        
        nearby_counter = False
    else:
        for loc in nearby_lst:
            loc.undraw()  
            
        nearby_lst = []
        nearby_counter = True
        
    return nearby_counter, nearby_lst
                
def toggle_other(enforcement_data, enforcement_lst, enforcement_counter, nearby, 
                 win):
    # Purpose: Show/hide the camera locations that are not on the route in the
    # graphical window
    # Parameters: Takes the camera location data, the camera points, bool
    # enforcement_counter, nearby data, and the graphical window win
    # Return: True or false enforcement_counter and the camera points
    
    if enforcement_counter:
        for loc in enforcement_data:
            if loc not in nearby:
                point = Point(float(loc[0]), float(loc[1]))
                dollar_other = Image(point, 'dollar_other.gif')
                enforcement_lst.append(dollar_other)
                enforcement_lst.append(point)
                dollar_other.draw(win)
                point.draw(win) 
                
        enforcement_counter = False
    else:
        for loc in enforcement_lst:
            loc.undraw()
            
        enforcement_lst = []
        enforcement_counter = True
    
    return enforcement_counter, enforcement_lst

main() # calls the main function when program runs