from beanie import Document, TimeSeriesConfig, Granularity
from datetime import datetime
from pydantic import UUID4
import os


class rawdata(Document):
    devicetime: datetime
    communityid: UUID4
    dwellingid: UUID4
    deviceid: UUID4
    data: dict
    meta: dict
    tz: str

    class Settings:
        name = os.getenv("CONSUMPTION_COLL")
        timeseries = TimeSeriesConfig(
            time_field="devicetime",
            meta_field="dwellingid",
            granularity=Granularity.seconds,
        )
        indexes = [
            "communityid",
            "dwellingid",
            "deviceid"
        ]
