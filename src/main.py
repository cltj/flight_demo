from flight_data import get_flight_data
from az_table import entity_crud
from schemas import Flight_Entry
import schedule
import time

# # # # # # # # # # # # # #
# Config
# # # # # # # # # # # # # #

connection_string = "<INSERT_CONNECTION_STRING>"
icao24="4b1807"


def main():
    data = get_flight_data(icao24)
    # Kompliser ting med pydantic her
    flight_data = Flight_Entry(data) # Trenger retting
    entity_crud(connection_string, table_name="<INSERT_TABLE_NAME>", operation='create', entity=flight_data)


if __name__ == "__main__":
    schedule.every(9).seconds.do(main())
    while True:
        schedule.run_pending()
        time.sleep(1)