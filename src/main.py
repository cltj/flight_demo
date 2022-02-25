from flight_data import single_flight_data
from az_table import entity_crud
from schemas import Flight_Entry
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
    flight_data = [Flight_Entry(**data)]
    #print(flight_data[0].icao24) # En test print
    entity_crud(connection_string, table_name=azure_table_name, operation='create', entity=flight_data[0])


if __name__ == "__main__":
    schedule.every(9).seconds.do(main()) #no kødd her, ellers bra
    while True:
        schedule.run_pending()
        time.sleep(1)