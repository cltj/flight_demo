from typing import Optional
from pydantic import BaseModel

class Flight_Entry(BaseModel):
    PartitionKey : str                              # Skal inneholde flight ID
    RowKey : str                                    # Skal inneholde tid (unix timestamp)
    icao24 : str or None
    callsign : str or None
    origin_country : str or None
    longitude : float or None
    latitude : float or None
    on_ground : Optional[bool or None]
    velocity : Optional[float or None]
    true_track : Optional[float or None]
    vertical_rate : Optional[float or None]
    geo_altitude : Optional[float or None]
    status : str or None                            # status col

class Not_Found_Entry(BaseModel):
    PartitionKey : str
    RowKey : str
    longitude : float or None
    latitude : float or None


# print(Flight_Entry.schema_json(indent=4))