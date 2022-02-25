from flight_data import single_flight_data
from az_table import entity_crud
from schemas import Flight_Entry
import schedule
import time
import os
from dotenv import load_dotenv #Fungerer ikke med poetry ???

# # # # # # # # # # # # # #
# Config
# # # # # # # # # # # # # #
# load_dotenv()
connection_string = "AZURE_TABLE_CONNECTION_STRING"
icao24="ICAO24"


def main():
    data = single_flight_data(icao24)
    # Kompliser ting med pydantic her
    flight_data = Flight_Entry(data) # Trenger retting
    entity_crud(connection_string, table_name="AZURE_TABLE_NAME", operation='create', entity=flight_data)


if __name__ == "__main__":
    schedule.every(9).seconds.do(main())
    while True:
        schedule.run_pending()
        time.sleep(1)