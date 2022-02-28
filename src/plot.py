import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from az_table import query_entities_values

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


def transform_data(data):
    df = pd.DataFrame(data, columns=["longitude", "latitude"])
    print(df.head())
    df = df.drop_duplicates(subset=["longitude", "latitude"], keep='last')
    return df


def plot(df, icao24):
    # initialize an axis
    fig, ax = plt.subplots(figsize=(8,8))
    # plot map on axis
    countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    countries[countries["name"] == "Sweden"].plot(color="darkgrey", ax=ax)
    # plot points
    fig = df.plot(
        x="longitude",
        y="latitude",
        kind="line",
        c="blue",
        #colormap="YlOrRd", jeg tror ikke denne linjen gjør noe akkurat nå
        title=f"Flight "+ str(icao24), #dette nummeret trengs å byttes ut med egen id når vi får det
        ax=ax
        ).get_figure()
    # add grid
    ax.grid(b=True, alpha=0.5)
    file_name = "./img/"+str(icao24)+".png"#si ifra hvis dette ikke fungerer på windows
    fig.savefig(file_name)#dette nummeret trengs å byttes ut med egen id når vi får det


def main():
    data = get_stored_flight_data(icao24=icao24)
    sorted_data = clean_and_sort(data)
    df = transform_data(sorted_data)
    plot(df,icao24)


if __name__ == "__main__":
    main()
