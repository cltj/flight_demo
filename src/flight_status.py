import os
from dotenv import load_dotenv
from flight_data import single_flight_data, now_in_unix_time

load_dotenv()
icao24 = os.getenv("ICAO24")


def flight_status(icao24):
    unix_timestamp = now_in_unix_time()
    # unix_timestamp = 1645865642 # for test
    data_1 = single_flight_data(icao24, unix_timestamp)
    data_2 = single_flight_data(icao24, unix_timestamp- int(300)) # Sjekker for 5 min siden
    if data_1[1] and data_2[1] == "OK":
        on_ground_1 = bool(data_1[0]['on_ground'])
        on_ground_2 = bool(data_2[0]['on_ground'])
        if on_ground_1 == True:
            if on_ground_2 == False:
                flight_status = "arrived" #kanskje lage egen ID tabell for flight status ???
                return flight_status
        if on_ground_1 ==  False:
            if on_ground_2 == False:
                flight_status = "enroute"
                return flight_status
        if on_ground_2 == True:
            if on_ground_1 == False:
                flight_status = "departed"
                return flight_status

#test1 = flight_status(icao24) # Arrived -time: 1645854809 + icao24: 4aca63
#print(test1)
#test2 = flight_status(icao24) # Enroute -time: 1645854627 + icao24: 4aca63
#print(test2)
test3 = flight_status(icao24) # Departed -time: 1645865642 + icao24: 4aca63
print(test3)