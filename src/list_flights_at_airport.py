import requests

def list_flights_at_airport(airport):
    baseUrl = "https://opensky-network.org/api/states/all?"
    bbox = u"lamin={}&lomin={}&lamax={}&lomax={}".format(airport["lamin"], airport["lomin"],airport["lamax"],airport["lomax"])
    print(airport["lomin"])    
    url = baseUrl + bbox
    response = requests.request("GET", url)
    flights_detected = []
    status_code = response.status_code
    if response.status_code == 200:
        json_data = response.json()
        if json_data['states'] == None:
            return "not found"
        else:
            for item in json_data['states']:
                flights_detected.append(item[0])
            return flights_detected
    else:
        msg = "Error: " + str(response)
        return msg

