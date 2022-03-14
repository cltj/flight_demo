import requests
import datetime
import time


def now_in_unix_time():
    presentDate = datetime.datetime.now()
    unix_timestamp = int(time.mktime(presentDate.timetuple()))-int(10) # 10 sekunder forsinkelse
    return unix_timestamp


def single_flight_data(icao24, unix_timestamp):
    """
    Calls API to get info on single icao24-identified flight
    Returns dict.
    """
    url = "https://opensky-network.org/api/states/all?time="+ str(unix_timestamp) + "&icao24=" + icao24
    payload={}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 200:
        json_data = response.json()
        x = json_data['states']
        if x == None:
            data = none_flight_values(icao24, unix_timestamp)
            msg = "not found"
            return data, msg
        else:
            data = extract_flight_values(json_data)
            msg = "OK"
            return data, msg
    else:
        print("Error with single flight data: " + str(status_code))


def get_on_ground(icao24, unix_timestamp):
    """
    Returns on ground status for icao24-identified flight
    Returns dict
    """
    url = "https://opensky-network.org/api/states/all?time="+ str(unix_timestamp) + "&icao24=" + icao24
    payload={}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 200:
        json_data = response.json()
        x = json_data['states']
        if x != None:
            on_ground_data = {}
            on_ground_data['icao24'] = str(x[0][0])
            on_ground_data['on_ground'] = str(x[0][8])
            return on_ground_data
    else:
        print("Error with single flight data: " + str(status_code))


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
    flight_data_dict['status'] = "MÅ SETTES INN" # Sjekker og setter inn status
    return flight_data_dict


def none_flight_values(icao24, unix_timestamp):
    flight_data_dict = {}
    flight_data_dict['PartitionKey'] = str(icao24)             # Needed for az-tables
    flight_data_dict['RowKey'] = unix_timestamp                # Needed for az-tables
    flight_data_dict['longitude'] = float(0.0)
    flight_data_dict['latitude'] = float(0.0)
    return flight_data_dict

single_flight_data("4784e8", now_in_unix_time())