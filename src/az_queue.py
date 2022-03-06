from config import My_Config
from azure.storage.queue import QueueClient

conn_str = My_Config.conn_str()


def new_departure(icao24):
    q_name = "flightdeparture"
    queue_client = QueueClient.from_connection_string(conn_str, q_name)
    queue_client.send_message(str(icao24))
    print("Departure: " + str(icao24))


def new_arrival(icao24):
    q_name = "flightarrival"
    queue_client = QueueClient.from_connection_string(conn_str, q_name)
    queue_client.send_message(str(icao24))
    print("Arrival: " + str(icao24))
