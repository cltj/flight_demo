from az_table import entity_crud
from config import My_Config

def get_airport_area(airport_id, tag):
    connection_string = My_Config.conn_str()
    azure_table_name = "airports"
    airport = {"PartitionKey" : airport_id, "RowKey": tag}

    response = entity_crud(connection_string, table_name=azure_table_name, operation='query', entity=airport)
    if response != None:
        lamin = str(response['lamin'])
        lomin = str(response['lomin'])
        lamax= str(response['lamax'])
        lomax = str(response['lomax'])
        return lamin, lomin, lamax, lomax
    else:
        print("Error: " + str(response))


# test
# x = get_airport_area("ABCDEF", "osl")
# print(x)
