import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from dotenv import load_dotenv
from az_table import query_entities_values
import seaborn as sns

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
    df = pd.DataFrame(data, columns=["longitude", "latitude", "geo_altitude", "time"])
    #altitude_df = pd.DataFrame(data, columns=["geo_altitude", "time"])
    print(df.head())
    #print(altitude_df.head())
    df = df.drop_duplicates(subset=["longitude", "latitude", "geo_altitude", "time"], keep='last')
    #altitude_df = altitude_df.drop_duplicates(subset=["geo_altitude", "time"], keep='last')
    return df


def plot(df, icao24):
    #TODO: Få vekk tallet i høyre hjørne, se på muligheten til å gi aksene ulik størrelse
    # initialize one figure with two axes
    fig, axs = plt.subplots(1, 2, figsize=(8,8), gridspec_kw=dict(width_ratios=[4, 3]))
    #plot the shape of sweden on the left axis    
    countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    countries[countries["name"] == "Sweden"].plot(color="darkgrey", ax=axs[0])
    #add grid
    axs[0].grid(b=True, alpha=0.5, c="black")
    #plot the data on the axes
    sns.scatterplot(data=df, x="longitude", y="latitude", ax=axs[0])
    sns.lineplot(data=df, x="time", y="geo_altitude", ax=axs[1])
    fig.tight_layout()
    #save file
    file_name = "./img/"+str(icao24)
    fig.savefig(file_name)#dette nummeret trengs å byttes ut med egen id når vi får det


def main():
    data = get_stored_flight_data(icao24=icao24)
    sorted_data = clean_and_sort(data)
    df = transform_data(sorted_data)
    plot(df, icao24)


if __name__ == "__main__":
    main()
