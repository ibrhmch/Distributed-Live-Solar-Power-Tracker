import requests
import json, jsonpickle
import os
import sys
import base64
import glob
import time, shutil
import csv
from time import strptime
from datetime import datetime
import uuid


#This program simulates inputs to the system using data from simualted solar sites in the year 2020. 
location_one = "../solar_data/C4C_22kw_data.csv"
location_two = "../solar_data/CHA_8kw_data.csv"
location_three = "../solar_data/EastCampus_40kw_data.csv"

REST = "localhost:5000"

def mkReq(reqmethod, endpoint, data, verbose=True):
    print(f"Response to http://{REST}/{endpoint} request is {type(data)}")
    jsonData = jsonpickle.encode(data)
    # jsonData = data
    if verbose and data != None:
        print(f"Make request http://{REST}/{endpoint} with json {data.keys()}")
        # print(f"mp3 is of type {type(data['mp3'])} and length {len(data['mp3'])} ")
    response = reqmethod(f"http://{REST}/{endpoint}", data=jsonData,
                         headers={'Content-type': 'application/json'})
    if response.status_code == 200:
        jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
        print(jsonResponse)
        return
    else:
        print(
            f"response code is {response.status_code}, raw response is {response.text}")
        return response.text
    
def getUID(reqmethod, endpoint, data, verbose=True):
    print(f"Response to http://{REST}/{endpoint} request is {type(data)}")
    jsonData = jsonpickle.encode(data)
    if verbose and data != None:
        print(f"Make request http://{REST}/{endpoint} with json {data.keys()}")
        print(f"mp3 is of type {type(data['mp3'])} and length {len(data['mp3'])} ")
    response = reqmethod(f"http://{REST}/{endpoint}", data=jsonData,
                         headers={'Content-type': 'application/json'})
    if response.status_code == 200:
        jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
        jsonResponse = json.loads(jsonResponse)
        # print(jsonResponse)
        return jsonResponse['UID']
    else:
        print(
            f"response code is {response.status_code}, raw response is {response.text}")
        return 0
    
with open(location_one, "r") as f_one, open(location_two, "r") as f_two, open(location_three, "r") as f_three:
    one_loc = {
        'lat' : 0,
        'lon' : 0
    }
    two_loc = {
        'lat' : 0,
        'lon' : 0
    }
    three_loc = {
        'lat' : 0,
        'lon' : 0
    }
    reader_one = csv.reader(f_one, delimiter=',')
    reader_two = csv.reader(f_two, delimiter=',')
    reader_three = csv.reader(f_three, delimiter=',')
    header_one = next(reader_one)
    header_two = next(reader_two)
    header_three = next(reader_three)
    # one_loc.append({'lat' : header_one[2], 'lon' : header_one[3]})
    one_loc['lat'] = header_one[2][1:]
    one_loc['lon'] = header_one[3][1:]
    two_loc['lat'] = header_two[2][1:]
    two_loc['lon'] = header_two[3][1:]
    three_loc['lat'] = header_three[2][1:]
    three_loc['lon'] = header_three[3][1:]
    # print("newdata/getUID/%s/%s" % (one_loc['lat'], one_loc['lon']))

    # UID_one = getUID(requests.get, "newdata/getUID/%s/%s" % ((one_loc['lat']), (one_loc['lon'])), data=None)
    # UID_two = getUID(requests.get, "newdata/getUID/%s/%s" % ((two_loc['lat']), (two_loc['lon'])), data=None)
    # UID_three = getUID(requests.get, "newdata/getUID/%s/%s" % ((three_loc['lat']), (three_loc['lon'])), data=None)

    UID_one = int(uuid.uuid4())
    to_send = {
        'panelId' : UID_one,
        'name' : "c4c Inout",
        'latitude' : float(one_loc['lat']),
        'longitude' : one_loc['lon']
    }
    print(to_send)
    mkReq(requests.post, "add_panel", data=(to_send))
    UID_two = int(uuid.uuid4())
    to_send = {
        'panelId' : UID_two,
        'name' : "Chataqua Input",
        'latitude' : two_loc['lat'],
        'longitude' : two_loc['lon']
    }
    mkReq(requests.post, "add_panel", data=(to_send))
    UID_three = int(uuid.uuid4())
    to_send = {
        'panelId' : UID_three,
        'name' : "East Campus input",
        'latitude' : three_loc['lat'],
        'longitude' : three_loc['lon']
    }
    mkReq(requests.post, "add_panel", data=(to_send))

    print(UID_one, UID_two, UID_three)
    for i in range(10):
        trash = input()
        for j in range(15):
            row_one = next(reader_one)
            row_two = next(reader_two)
            row_three = next(reader_three)
            data_payload_one = {
                'year' : 0,
                'month' : 0,
                'day' : 0,
                'hour' : 0,
                'minute' : 0,
                'generation' : 0,
                'capacity' : 0,
            }
            data_payload_two = {
                'year' : 0,
                'month' : 0,
                'day' : 0,
                'hour' : 0,
                'minute' : 0,
                'generation' : 0,
                'capacity' : 0,
            }
            data_payload_three = {
                'year' : 0,
                'month' : 0,
                'day' : 0,
                'hour' : 0,
                'minute' : 0,
                'generation' : 0,
                'capacity' : 0,
            }
            # date = row_one[0].split(',')
            # print("Date: ", date)
            # time_curr = date[1][1:]
            # in_time = datetime.strptime(time_curr, "%I:%M %p")
            # out_time = datetime.strftime(in_time, "%H:%M")
            # # print("Time: ", out_time)


            # data_payload['year'] = '2020'
            # data_payload['month'] = str(strptime(date[0].split(' ')[0],'%b').tm_mon)
            # data_payload['day'] = (date[0].split(' ')[1])
            # data_payload['hour'] = (out_time.split(':')[0])
            # data_payload['minute'] = (out_time.split(':')[1])
            data_payload_one['generation'] = str(abs(float(row_one[1])))
            data_payload_two['generation'] = str(abs(float(row_two[1])))
            data_payload_three['generation'] = str(abs(float(row_three[1])))
            # data_payload['capacity'] = '22'
            # mkReq(requests.post, "newdata/%s" % (UID_one), data=data_payload)
            # get_req = "pulldata/%s/%s/%s/%s/%s/%s" % (UID_one, data_payload['year'], data_payload['month'], data_payload['day'],data_payload['hour'], data_payload['minute'])
            # mkReq(requests.get, get_req, data=None)
        # mkReq(requests.get, "pulldata/getUID/40.00/41.00/104.00/106.00", data=None)
            to_send_one = {
                'panelId' : UID_one,
                'powerKw' : data_payload_one['generation']
            }
            to_send_two = {
                'panelId' : UID_two,
                'powerKw' : data_payload_two['generation']
            }
            to_send_three = {
                'panelId' : UID_three,
                'powerKw' : data_payload_three['generation']
            }
            print("Ready for next new data!")
            
            mkReq(requests.post, "add_panel_data", data=(to_send_one))
            mkReq(requests.post, "add_panel_data", data=(to_send_two))
            mkReq(requests.post, "add_panel_data", data=(to_send_three))
        