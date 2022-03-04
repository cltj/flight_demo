from config import My_Config
from azure.storage.queue import QueueClient
from flight_data import now_in_unix_time

conn_str = My_Config.conn_str()
q_name = "flightsqueue"


def new_departure(icao24):
    now = now_in_unix_time()
    queue_client = QueueClient.from_connection_string(conn_str, q_name)
    msg = "departure." + icao24 + "." + str(now)
    queue_client.send_message(msg)


def new_arrival(icao24):
    now = now_in_unix_time()
    queue_client = QueueClient.from_connection_string(conn_str, q_name)
    msg = "arrival." + icao24 + "." + str(now)
    queue_client.send_message(msg)
    print(msg)
