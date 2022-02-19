from logging import exception
from xmlrpc.client import DateTime
import pandas as pd
import requests
#import pydantic
import datetime
import time
import json


def get_flight_data(icao24):
    presentDate = datetime.datetime.now()
    unix_timestamp = int(time.mktime(presentDate.timetuple()))

    url = "https://opensky-network.org/api/states/all?time="+str(unix_timestamp)+ "&icao24=" + icao24

    payload={}
    headers = {
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 200:
        json_data = response.json()
        x = json_data['states']
        return json_data
    else:
        return response.status_code

def main():
    icao24="4952c1"
    flight_data = get_flight_data(icao24)
    print(flight_data['time'])
    print(flight_data['states'])

if __name__ == "__main__":
    main()