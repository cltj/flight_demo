from flight_data import get_on_ground, now_in_unix_time
from az_queue import new_departure, new_arrival

enroute_list = []

def flight_status(icao24):
    enroute = True if icao24 in enroute_list else False
    if enroute == True:
        has_arrived = check(icao24)
        if has_arrived == True:
            enroute_list.remove(icao24)
        else:
            pass
    else:
        has_departed = check(icao24)
        if has_departed == True:
            enroute_list.append(icao24)
        else:
            pass


def check(icao24):
    """
    Checks if flight has arrived/departed by checking on-ground status now and 5 minutes ago
    Removes flight from enroute_list in case arrival, adds flight in case departure
    """
    unix_timestamp = now_in_unix_time()
    data_1 = get_on_ground(icao24, unix_timestamp)
    data_2 = get_on_ground(icao24, unix_timestamp- int(300)) # Sjekker for 5 min siden
    if data_1 and data_2 is not None:
        d1_ground = data_1['on_ground']
        d2_ground = data_2['on_ground']
        if d1_ground == d2_ground:
            msg = str(icao24 + ": Equal values, skipping...")
            print(msg)
            pass
        elif d1_ground == 'True':
            if d2_ground == 'False':
                msg = str(icao24 + ": Plane has arrived in the last 5 minutes")
                print(msg)
                enroute_list.remove(icao24)
                new_arrival(icao24)
                return True
        elif d2_ground ==  'True':
            if d1_ground == 'False':
                msg = str(icao24 + ": Plane has departed in the last 5 minues")
                print(msg)
                enroute_list.append(icao24)
                new_departure(icao24)
                return True
        else:
            print("Error in flight status")
    else:
        msg = str(icao24 + ": None value found, skipping...")
        print(msg)


def trip_tracker():
    return enroute_list