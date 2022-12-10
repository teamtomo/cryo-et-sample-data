import os
import textwrap
from typing import Any, Dict

import numpy as np
import pooch
from pooch import Pooch

from cryo_et_sample_data.utils import DataItem, DataSetConfig


def build_registry_dict_from_config(data: DataSetConfig) -> Dict[str, str]:
    registry = dict()

    if data.tomogram is not None:
        registry[data.tomogram.file_name] = data.tomogram.checksum

    return registry


class DataSet:
    _CACHE_BASE_PATH: str = "cryo_et_sample_data"

    def __init__(
        self,
        name: str,
        author: str,
        description: str,
        base_url: str,
        tomogram: DataItem,
    ):
        self._config = DataSetConfig(
            name=name,
            author=author,
            description=description,
            base_url=base_url,
            tomogram=tomogram,
        )

        registry_dict = build_registry_dict_from_config(self._config)
        cache_path = os.path.join(self._CACHE_BASE_PATH, name)
        self._registry: Pooch = pooch.create(
            path=pooch.os_cache(cache_path),
            base_url=base_url,
            registry=registry_dict,
        )

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def base_url(self) -> str:
        return self._config.base_url

    @property
    def author(self) -> str:
        return self._config.author

    @property
    def description(self) -> str:
        return self._config.description

    def _get_data(self, data_name: str) -> str:
        data_item: DataItem = getattr(self._config, data_name)
        if data_item is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} doesn't have a {data_name}"
            )
        return self._registry.fetch(data_item.file_name, progressbar=True)

    @property
    def tomogram(self) -> np.ndarray:
        tomogram_path = self._get_data("tomogram")
        return self._config.tomogram.reader(tomogram_path)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]):
        return cls(**config_dict)

    def _string_representation(self) -> str:
        result = "cryoET DataSet\n"

        result += f"\tname: {self.name}\n"
        result += f"\tauthor: {self.author}\n"
        result += f"\tbase url: {self.base_url}\n"

        description_wrapped = textwrap.wrap(self.description)
        result += "\n\tDescription:\n\t  "
        result += "\n\t  ".join(description_wrapped) + "\n"

        result += "\n\tdata\n"

        if self._config.tomogram is not None:
            result += "\t  └── tomogram\n"
            result += (
                f"\t\t  ├── file name: {self._config.tomogram.file_name}\n"
            )
            result += f"\t\t  └── checksum: {self._config.tomogram.checksum}\n"

        return result

    def __str__(self) -> str:
        return self._string_representation()
