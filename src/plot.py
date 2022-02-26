import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from az_table import query_entities_values
from PIL import Image


# # # # # # #
# Config    #
# # # # # # #

load_dotenv()
connection_string = os.getenv("AZURE_TABLE_CONNECTION_STRING")
azure_table_name = os.getenv("AZURE_TABLE_NAME")
icao24 = os.getenv("ICAO24")


def get_stored_flight_data(icao24):
    partition_key = str("'"+icao24+"'")
    filter = "PartitionKey eq {}".format(partition_key)
    select = u"PartitionKey, time, longitude, latitude, on_ground, geo_altitude"
    data = query_entities_values(connection_string=connection_string,table_name=azure_table_name, select=select, filter=filter)
    return data


def clean_and_sort(data):
    lst = []
    for item in data:
        if item['time'] != None:
            lst.append(item)
        else:
            pass
    sorted_data = sorted(lst, key=lambda d: d['time'])
    return sorted_data


def vector(first_entity,last_entity):
    flight_time = last_entity[0]['time']-first_entity[0]['time']
    horizontal_travel = first_entity[0]['latitude']-last_entity[0]['latitude']
    vertical_travel = first_entity[0]['longitude']-last_entity[0]['longitude']
    print(" flight time: {} \n lat: {} \n long: {}".format(flight_time,horizontal_travel,vertical_travel))


def transform_data(data):
    #df = pd.DataFrame(data, columns=["PartitionKey", "time", "longitude", "latitude", "on_ground", "geo_altitude"])
    df = pd.DataFrame(data, columns=["longitude", "latitude"])
    df = df.drop_duplicates(subset=["longitude", "latitude"], keep='last')
    return df


def plot(df):
    BBox = (df.longitude.min(), df.longitude.max(), df.latitude.min(), df.latitude.max())
    # Plot the data


def main():
    data = get_stored_flight_data(icao24=icao24)
    sorted_data = clean_and_sort(data)
    first_entity = sorted_data[:1:1]
    last_entity = sorted_data[len(sorted_data)-1::1]
    vector(first_entity,last_entity)

    df = transform_data(sorted_data)
    print(df)
    with Image.open("C:\\Users\\thki01\\Downloads\\this-map.png") as im:
        im.rotate(45).show()
    #plot(df)


if __name__ == "__main__":
    main()
