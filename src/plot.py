import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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
    altitude_df = pd.DataFrame(data, columns=["geo_altitude", "time"])
    print(df.head())
    print(altitude_df.head())
    df = df.drop_duplicates(subset=["longitude", "latitude"], keep='last')
    altitude_df = altitude_df.drop_duplicates(subset=["geo_altitude", "time"], keep='last')
    return df, altitude_df

#TODO: Legg til et subplot(?) med altitude
def plot(df, altitude_df, icao24):
    # initialize an axis
    fig, ax = plt.subplots(figsize=(8,8))
    fig2, ax2 = plt.subplots(figsize=(8,8))
    # plot map on axis
    countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    countries[countries["name"] == "Sweden"].plot(color="darkgrey", ax=ax)
    # plot points
    fig = df.plot(
        x="longitude",
        y="latitude",
        kind="scatter",
        c="blue",
        colormap="YlOrRd",
        title="Flight "+ str(icao24), #dette nummeret trengs å byttes ut med egen id når vi får det
        ax=ax
        ).get_figure()
    #plot second figure
    fig2 = altitude_df.plot(
        x="time",
        y="geo_altitude",
        c="blue",
        ax=ax2,
    ).get_figure()
    # add grid
    ax.grid(b=True, alpha=0.5)
    file_name = "./img/"+str(icao24)#si ifra hvis dette ikke fungerer på windows
    save_two_figs(file_name)#dette nummeret trengs å byttes ut med egen id når vi får det

def save_two_figs(filename):
    #hadde vært fint å fått som .png med begge, heller en pdf med to sider
    pdf = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(pdf, format='pdf')
    pdf.close()

def main():
    data = get_stored_flight_data(icao24=icao24)
    sorted_data = clean_and_sort(data)
    df, altitude_df = transform_data(sorted_data)
    plot(df, altitude_df, icao24)


if __name__ == "__main__":
    main()
