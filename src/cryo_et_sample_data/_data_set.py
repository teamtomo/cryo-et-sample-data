import os
from typing import Any, Callable, Dict, Optional

import numpy as np
import pooch
from pooch import Pooch
from pydantic import BaseModel, Field, PrivateAttr, validator

from cryo_et_sample_data.utils import word_wrap_with_line_breaks


class FileMetadata(BaseModel):
    """Metadata for a piece of data in a DataSet.

    Note: all fields are immutable.

    Attributes
    ----------
    file_name : str
        The file name for the data. The file should
        be findable at base_url/file_name
    checksum : str
        The checksum for the datum.
    reader : Callable
        The function used to load the data from disk.
    """

    file_name: str = Field(allow_mutation=False)
    checksum: str = Field(allow_mutation=False)
    reader: Callable = Field(allow_mutation=False)

    class Config:
        """validate assignments to make fields immutable"""

        validate_assignment = True


class DataSet(BaseModel):
    """A lazy, cached downloader for a set of tomography data.

    Currently supported data:
        - tomogram: the reconstructed image.

    Attributes
    ----------
    name : str
        The name of the DataSet. Spaces are not allowed.
    base_url : str
        The url to access the dataset. See the pooch
        documentation for the valid formats.
    author : str
        The author(s) of the dataset.
    description : str
        A description of the dataset. This should be
        a contiuous string without line breaks. The
        DataSet class will automatically apply word
        wrapping.
    tomogram_metadata : Optional[FileMetadata]
        The metadata for the tomogram dataset.
        If None, no tomogram is included.
        Default value is None.
    label_metadata : Optional[FileMetadata]
        The metadata for the label image. If None,
        no label data is included.
        Default value is None.
    """

    name: str = Field(allow_mutation=False)
    base_url: str = Field(allow_mutation=False)
    author: str = Field(allow_mutation=False)
    description: str = Field(allow_mutation=False)
    tomogram_metadata: Optional[FileMetadata] = Field(
        None, allow_mutation=False
    )
    label_metadata: Optional[FileMetadata] = Field(None, allow_mutation=False)

    _registry: Pooch = PrivateAttr()
    _CACHE_BASE_PATH: str = PrivateAttr("cryo_et_sample_data")

    class Config:
        """validate assignments to make fields immutable"""

        validate_assignment = True

    def __init__(
        self,
        name: str,
        author: str,
        description: str,
        base_url: str,
        tomogram_metadata: Optional[FileMetadata] = None,
        label_metadata: Optional[FileMetadata] = None,
    ):
        # parse the input
        super().__init__(
            name=name,
            author=author,
            description=description,
            base_url=base_url,
            tomogram_metadata=tomogram_metadata,
            label_metadata=label_metadata,
        )

        # make the pooch registry
        registry_dict = self._build_registry_dict()
        cache_path = os.path.join(self._CACHE_BASE_PATH, name)
        self._registry: Pooch = pooch.create(
            path=pooch.os_cache(cache_path),
            base_url=base_url,
            registry=registry_dict,
        )

    @property
    def tomogram(self) -> np.ndarray:
        """The tomogram image.

        If no tomogram image is included in the dataset,
        this raises a NotImplementedError.

        Returns
        -------
        tomogram : np.ndarray
            The tomogram image.
        """
        tomogram_path = self._get_data("tomogram")
        return self.tomogram_metadata.reader(tomogram_path)

    @property
    def label(self) -> np.ndarray:
        """The label image.

        If no label image is included in the dataset,
        this raises a NotImplementedError.

        Returns
        -------
        label : np.ndarray
            The label image.
        """
        label_path = self._get_data("label")
        return self.label_metadata.reader(label_path)

    def _get_data(self, data_name: str) -> str:
        """Download a given datum (if not cached) and return
        the file path to the data.

        If the datum is not present in this dataset, this
        raises a NotImplementedError.

        Parameters
        ----------
        data_name : str
            The name of the data to fetch.

        Returns
        -------
        file_path : str
            The path to the downloaded file.
        """
        data_item: FileMetadata = getattr(self, f"{data_name}_metadata")
        if data_item is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} doesn't have a {data_name}"
            )
        return self._registry.fetch(data_item.file_name, progressbar=True)

    def _build_registry_dict(self) -> Dict[str, str]:
        """Build the pooch data registry dictionary from
        the model fields.

        Returns
        -------
        registry : Dict[str, str]
            The pooch registry dictionary where the keys
            are the file name and the values are the checksum.
        """
        registry = dict()

        if self.tomogram_metadata is not None:
            registry[
                self.tomogram_metadata.file_name
            ] = self.tomogram_metadata.checksum
        if self.label_metadata is not None:
            registry[
                self.label_metadata.file_name
            ] = self.tomogram_metadata.checksum

        return registry

    @validator("name", pre=True)
    def _check_for_spaces_in_name(cls, v):
        if " " in v:
            raise ValueError("spaces are not allowed in name")
        return v

    @validator("tomogram_metadata", pre=True)
    def _coerce_data_item(cls, v):
        """Coerce a DataItem field to the correct type"""
        if isinstance(v, dict):
            return FileMetadata(**v)
        else:
            return v

    def _string_representation(self) -> str:
        """Construct the string representation of the DataSet.
        This is used by the __str__ and __repr__ methods
        """
        indent = "    "
        result = "cryoET DataSet\n"

        result += f"{indent}name: {self.name}\n"
        result += f"{indent}author: {self.author}\n"
        result += f"{indent}base url: {self.base_url}\n"

        description_wrapped = word_wrap_with_line_breaks(
            self.description,
            paragraph_width=60,
        )
        result += f"\n{indent}description:\n{2*indent}"
        result += f"\n{2*indent}".join(description_wrapped) + "\n"

        result += f"\n{indent}data\n"

        if self.tomogram_metadata is not None:
            result += f"{indent}  └── tomogram\n"
            result += (
                f"{2*indent}  ├── file name: "
                f"{self.tomogram_metadata.file_name}\n"
            )
            result += (
                f"{2*indent}  └── checksum: "
                f"{self.tomogram_metadata.checksum}\n"
            )

        return result

    def __repr__(self) -> str:
        return self._string_representation()

    def __str__(self) -> str:
        return self._string_representation()

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]):
        """Convenience method to construct from a dictionary."""
        return cls(**config_dict)
