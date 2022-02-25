import requests
import datetime
import time


def single_flight_data(icao24):
    presentDate = datetime.datetime.now()
    unix_timestamp = int(time.mktime(presentDate.timetuple()))-int(10) # 10 sekunder forsinkelse

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
            return resp
        else:
            data = extract_flight_values(json_data)
            return data
    else:
        return resp


def extract_flight_values(flight_data):
    flight_data_dict = {}
    flight_data_dict['PartitionKey'] = str(flight_data['states'][0][1])             # Needed for az-tables
    flight_data_dict['RowKey'] = flight_data['time']                                # Needed for az-tables
    flight_data_dict['time'] = flight_data['time']
    flight_data_dict['icao24'] = str(flight_data['states'][0][0])
    flight_data_dict['callsign'] = str(flight_data['states'][0][1])
    flight_data_dict['origin_country'] = str(flight_data['states'][0][2])
    flight_data_dict['time_position'] = int(flight_data['states'][0][3])
    flight_data_dict['last_contact'] = int(flight_data['states'][0][4])
    flight_data_dict['longitude'] = float(flight_data['states'][0][5])
    flight_data_dict['latitude'] = float(flight_data['states'][0][6])
    flight_data_dict['baro_altitude'] = flight_data['states'][0][7]
    flight_data_dict['on_ground'] = bool(flight_data['states'][0][8])
    flight_data_dict['velocity'] = float(flight_data['states'][0][9])
    flight_data_dict['true_track'] = float(flight_data['states'][0][10])
    flight_data_dict['vertical_rate'] = flight_data['states'][0][11]
    flight_data_dict['sensors'] = flight_data['states'][0][12]
    flight_data_dict['geo_altitude'] = flight_data['states'][0][13]
    flight_data_dict['squawk'] = str(flight_data['states'][0][14])
    flight_data_dict['spi'] = bool(flight_data['states'][0][15])
    flight_data_dict['position_source'] = int(flight_data['states'][0][16])
    return flight_data_dict