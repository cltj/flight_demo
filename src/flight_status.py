from flight_data import get_on_ground, now_in_unix_time
from az_queue import new_departure, new_arrival


def flight_status(icao24):
    unix_timestamp = now_in_unix_time()
    data_1 = get_on_ground(icao24, unix_timestamp)
    data_2 = get_on_ground(icao24, unix_timestamp- int(300)) # Sjekker for 5 min siden

    if data_1 and data_2 is not None:
        d1_ground = data_1['on_ground']
        d2_ground = data_2['on_ground']
        if d1_ground == d2_ground:
            if d1_ground == 'True':
                msg = str(icao24 + ": Plane has been on the ground for 5 minutes")
                print(msg)
            else:
                msg = str(icao24 + ": Plane has been in the air for the last 5 minutes")
                print(msg)
        elif d1_ground == 'True':
            if d2_ground == 'False':
                msg = str(icao24 + ": Plane has arrived in the last 5 minutes")
                print(msg)
                new_arrival(icao24)
        elif d2_ground ==  'True':
            if d1_ground == 'False':
                msg = str(icao24 + ": Plane has departed in the last 5 minues")
                print(msg)
                new_departure(icao24)
        else:
            print("Error in flight status")
    else:
        msg = str(icao24 + ": None value found, skipping...")
        print(msg)
