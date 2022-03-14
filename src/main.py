from flight_data import single_flight_data, now_in_unix_time
from list_flights import list_flights
from flight_status import flight_status
from config import My_Config
from az_table import list_entities
from schemas import Flight_Entry, Not_Found_Entry
import schedule
import time


def check_status(airport_id, tag):
    flights = list_flights(airport_id, tag)
    for flight in flights:
        print(str(len(flights)) + " fligths in list")
        flights.pop(0)
        flight_status(flight)


def main():
    airports = list_entities(connection_string=My_Config.conn_str(), table_name="airports", select="*")
    for airport in airports:
        check_status(airport_id=airport['PartitionKey'],tag=airport['RowKey'])
    print("Done!!!")
    """
    unix_timestamp = now_in_unix_time()
    data = single_flight_data(icao24, unix_timestamp)
    if data[1] != "OK":
        print(data[1])
        flight_data = [Not_Found_Entry(**data[0])]
        entity_crud(connection_string, table_name=azure_table_name, operation='create', entity=flight_data[0])
    else:
        flight_data = [Flight_Entry(**data[0])]
        print("Lat/Long: "+str(flight_data[0].latitude)+","+str(flight_data[0].longitude)) # En test print
        entity_crud(connection_string, table_name=azure_table_name, operation='create', entity=flight_data[0])
"""

if __name__ == "__main__":
    schedule.every(5).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)