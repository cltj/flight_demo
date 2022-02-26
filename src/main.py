from flight_data import single_flight_data
from az_table import entity_crud
from schemas import Flight_Entry, Not_Found_Entry
import schedule
import time
import os
from dotenv import load_dotenv

# # # # # # # # # # # # # #
# Config
# # # # # # # # # # # # # #
load_dotenv()
connection_string = os.getenv("AZURE_TABLE_CONNECTION_STRING")
azure_table_name = os.getenv("AZURE_TABLE_NAME")
icao24 = os.getenv("ICAO24")


def main():
    data = single_flight_data(icao24)
    if data[1] != "OK":
        print(data[1])
        flight_data = [Not_Found_Entry(**data[0])]
        entity_crud(connection_string, table_name=azure_table_name, operation='create', entity=flight_data[0])
    else:
        flight_data = [Flight_Entry(**data[0])]
        print("Lat/Long: "+str(flight_data[0].latitude)+","+str(flight_data[0].longitude)) # En test print
        entity_crud(connection_string, table_name=azure_table_name, operation='create', entity=flight_data[0])


if __name__ == "__main__":
    schedule.every(60).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)