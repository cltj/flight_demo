from az_table import entity_crud
from config import My_Config
import uuid

from new_flight import new_guid

# 1. Insert coordinates
# 2. Make bounding box
# 3. Add to airports table
# 4. List all airports
# 5. For each airport find flights within bounding box
# 6. Return list of flights

class Airport():
    def __init__(self, airport_id, lat, lon):
        self.airport_id = airport_id
        self.lat = lat
        self.lon = lon


    def uuid_gen(self):
        """Generates a UUID"""
        return uuid.uuid4()


    def make_bounding_box(self, lat, lon):
        """Makes a bounding box from coordinates(lat,lon)"""
        lamin = lat - 0.7
        lomin = lon - 0.7
        lamax = lat + 0.7
        lomax = lon + 0.7
        return lamin, lomin, lamax, lomax


def add_airport(Airport, lat, lon):
    """Adds an airport to the airports table"""
    lamin, lomin, lamax, lomax = Airport().make_bounding_box(lat, lon)
    airport = [airport_id, tag, lamin, lomin, lamax, lomax]
    connection_string = My_Config.conn_str()
    azure_table_name = "airports"
    response = entity_crud(connection_string, table_name=azure_table_name, operation='insert', entity=airport)
    if response != None:
        print("Airport added")
    else:
        print("Error: " + str(response))

