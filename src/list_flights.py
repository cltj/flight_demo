import requests
from airport_area import get_airport_area


def list_flights(airport_id, tag):
    lamin, lomin, lamax, lomax = get_airport_area(airport_id,tag)
    baseUrl = "https://opensky-network.org/api/states/all?"
    bbox = u"lamin={}&lomin={}&lamax={}&lomax={}".format(lamin,lomin,lamax,lomax)
    url = baseUrl + bbox
    payload={}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    flights_detected = []
    status_code = response.status_code
    if status_code == 200:
        json_data = response.json()
        x = json_data['states']
        if x == None:
            return "not found"
        else:
            for item in json_data['states']:
                flights_detected.append(item[0])
            return flights_detected
    else:
        msg = "Error: " + str(response)
        return msg


# Test
#x = list_flights("ABCDEF","osl")
#print(x)