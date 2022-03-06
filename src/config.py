import os
from dotenv import load_dotenv


class My_Config():
    load_dotenv()
    def conn_str():
        connection_string = os.getenv("AZURE_TABLE_CONNECTION_STRING")
        return connection_string
    def table():
        azure_table_name = os.getenv("AZURE_TABLE_NAME")
        return azure_table_name
    def icao24():
        icao24 = os.getenv("ICAO24")
        return icao24
    def queue():
        azure_queue_name = os.getenv("AZURE_QUEUE_NAME")
        return azure_queue_name