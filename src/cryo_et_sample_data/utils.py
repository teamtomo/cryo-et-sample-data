from dataclasses import dataclass
from typing import Callable, Optional

from pydantic import BaseModel, validator


@dataclass
class DataEntry:
    file_name: str
    checksum: str
    reader: Callable


@dataclass
class TomographyData:
    tomogram: Optional[DataEntry] = None


class DataItem(BaseModel):
    file_name: str
    checksum: str
    reader: Callable


class DataSetConfig(BaseModel):
    name: str
    base_url: str
    author: str
    tomogram: Optional[DataItem] = None

    @validator("tomogram", pre=True)
    @classmethod
    def _coerce_data_item(cls, v):
        """Coerce a DataItem field to the correct type"""
        if isinstance(v, dict):
            return DataItem(**v)
        else:
            return v
