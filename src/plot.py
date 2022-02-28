import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.image as pli
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
    print(df.head())
    df = df.drop_duplicates(subset=["longitude", "latitude"], keep='last')
    return df


def plot(df):
    # initialize an axis
    fig, ax = plt.subplots(figsize=(8,6))
    # plot map on axis
    countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    countries[countries["name"] == "Sweden"].plot(color="lightgrey", ax=ax)
    # plot points
    fig = df.plot(
        x="longitude",
        y="latitude",
        kind="scatter",
        c="blue",
        colormap="YlOrRd",
        title=f"Flight",
        ax=ax
        ).get_figure()
    # add grid
    ax.grid(b=True, alpha=0.5)
    fig.savefig('test.png')



def main():
    data = get_stored_flight_data(icao24=icao24)
    sorted_data = clean_and_sort(data)
    first_entity = sorted_data[:1:1]
    last_entity = sorted_data[len(sorted_data)-1::1]
    vector(first_entity,last_entity)

    df = transform_data(sorted_data)
    plot(df)


if __name__ == "__main__":
    main()
