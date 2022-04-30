from numpy import true_divide
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

class Airports(object):
    
    def __init__(self):
        self.airport_ids = []
        self.flight_id = []

    def new_guid():
        """returns a unique id (uuid)"""
        new_id = uuid.uuid4()
        return new_id

    
    def list_airports():
        """list airports"""
        return airport_ids


    def find_flight():
        """find flight"""
        return flight_id
    
    
    def add_airport_to_list():
        """add airport to list"""
        airport_id = new_guid()
        return air

    
    def create_bounding_box(airport_id, tag):
        connection_string = My_Config.conn_str()
        azure_table_name = "airports"
        airport = {"PartitionKey" : airport_id, "RowKey": tag}

        response = entity_crud(connection_string, table_name=azure_table_name, operation='query', entity=airport)
        if response != None:
            lamin = str(response['lamin'])
            lomin = str(response['lomin'])
            lamax= str(response['lamax'])
            lomax = str(response['lomax'])
            return [lamin, lomin, lamax, lomax]
        else:
            print("Error: " + str(response))
