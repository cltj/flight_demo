import requests
import datetime
import time
from flight_status import flight_status


def now_in_unix_time():
    presentDate = datetime.datetime.now()
    unix_timestamp = int(time.mktime(presentDate.timetuple()))-int(10) # 10 sekunder forsinkelse
    return unix_timestamp


def single_flight_data(icao24, unix_timestamp):
    url = "https://opensky-network.org/api/states/all?time="+ str(unix_timestamp) + "&icao24=" + icao24
    payload={}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    resp = requests.request("GET", 'https://http.cat/'+ str(status_code))
    if status_code == 200:
        json_data = response.json()
        x = json_data['states']
        if x == None:
            resp = requests.request("GET", 'https://http.cat/400')
            data = none_flight_values(icao24, unix_timestamp)
            msg = "not found"
            return data, msg, resp
        else:
            data = extract_flight_values(json_data)
            msg = "OK"
            return data, msg, resp
    else:
        return resp


def extract_flight_values(flight_data): # legg til id her
    flight_data_dict = {}
    flight_data_dict['PartitionKey'] = str(flight_data['states'][0][0])             # Needed for az-tables (id)
    flight_data_dict['RowKey'] = flight_data['time']                                # Needed for az-tables (time)
    flight_data_dict['icao24'] = str(flight_data['states'][0][0])
    flight_data_dict['callsign'] = str(flight_data['states'][0][1])
    flight_data_dict['origin_country'] = str(flight_data['states'][0][2])
    flight_data_dict['longitude'] = float(flight_data['states'][0][5])
    flight_data_dict['latitude'] = float(flight_data['states'][0][6])
    flight_data_dict['on_ground'] = bool(flight_data['states'][0][8])
    flight_data_dict['velocity'] = float(flight_data['states'][0][9])
    flight_data_dict['true_track'] = float(flight_data['states'][0][10])
    flight_data_dict['vertical_rate'] = flight_data['states'][0][11]
    flight_data_dict['geo_altitude'] = flight_data['states'][0][13]
    flight_data_dict['status'] = flight_status(str(flight_data['states'][0][0])) # Sjekker og setter inn status
    return flight_data_dict


def none_flight_values(icao24, unix_timestamp):
    flight_data_dict = {}
    flight_data_dict['PartitionKey'] = str(icao24)             # Needed for az-tables
    flight_data_dict['RowKey'] = unix_timestamp                # Needed for az-tables
    flight_data_dict['longitude'] = float(0.0)
    flight_data_dict['latitude'] = float(0.0)
    return flight_data_dict