from az_table import entity_crud, list_entities
from config import My_Config
from generate import random_char

# 1. Insert coordinates
# 2. Make bounding box and ID
# 3. Add to airports table
# 4. List all airports


def make_bounding_box(lat, lon):
    """Makes a bounding box from coordinates(lat,lon)"""
    lamin = lat - 0.7
    lomin = lon - 0.7
    lamax = lat + 0.7
    lomax = lon + 0.7
    return [lamin, lomin, lamax, lomax]


def add_airport(lat, lon):
    """Add airport from coordinates(lat,lon)"""
    bbox = make_bounding_box(lat, lon)
    airport = {"PartitionKey": "Airport", "RowKey": random_char(5), "lamin": round(bbox[0], 4), "lomin": round(bbox[1], 4), "lamax": round(bbox[2], 4), "lomax": round(bbox[3], 4)}
    connection_string = My_Config.conn_str()
    response = entity_crud(connection_string, table_name="airports", operation='create', entity=airport)
    if response != None:
        print("Success: " + str(response))
    else:
        print("Error: " + str(response))


def list_airports():
    """List all airports"""
    connection_string = My_Config.conn_str()
    airports = list_entities(connection_string, table_name="airports", select="*")
    return airports
