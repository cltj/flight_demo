from typing import Optional
from pydantic import BaseModel

class Flight_Entry(BaseModel):
    PartitionKey : str
    RowKey : str
    time : int or None
    icao24 : str or None
    callsign : str or None
    origin_country : str or None
    time_position : int or None
    last_contact : int or None
    longitude : float or None
    latitude : float or None
    baro_altitude : Optional[float or None]
    on_ground : Optional[bool or None]
    velocity : Optional[float or None]
    true_track : Optional[float or None]
    vertical_rate : Optional[float or None]
    sensors : Optional[int or None]
    geo_altitude : Optional[float or None]
    squawk : Optional[str or None]
    spi : Optional[bool or None]
    position_source : Optional[int or None]

class Not_Found_Entry(BaseModel):
    PartitionKey : str
    RowKey : str
    longitude : float or None
    latitude : float or None


# print(Flight_Entry.schema_json(indent=4))