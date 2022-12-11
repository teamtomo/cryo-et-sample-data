import mrcfile
import pytest
from pydantic import ValidationError

from cryo_et_sample_data._data_set import DataSet, FileMetadata


def test_file_metadata():
    metadata = FileMetadata(
        file_name="test.zarr",
        checksum="mic_check_one_two",
        reader=mrcfile.read,
    )

    # fields should be immutable
    with pytest.raises(TypeError):
        metadata.file_name = "new.zarr"
    with pytest.raises(TypeError):
        metadata.checksum = "new_checksum"
    with pytest.raises(TypeError):
        metadata.reader = mrcfile.open


def test_invalid_file_metadata_reader():
    """FileMetadata.reader must be a callable"""
    with pytest.raises(ValidationError):
        _ = FileMetadata(
            file_name="test.zarr",
            checksum="mic_check_one_two",
            reader="mrcfile.read",
        )


test_config_dict = {
    "name": "hiv",
    "author": "Alister Burt",
    "description": "really good data",
    "base_url": "doi:10.5281/zenodo.6504891/",
    "tomogram_metadata": {
        "file_name": "01_10.00Apx.mrc",
        "checksum": "md5:426325d006fe04276ea01df9d83ad510",
        "reader": mrcfile.read,
    },
}


def test_data_set():
    tomogram_metadata = FileMetadata(
        file_name="01_10.00Apx.mrc",
        checksum="md5:426325d006fe04276ea01df9d83ad510",
        reader=mrcfile.read,
    )

    data_set = DataSet(
        name="hiv",
        author="Alister Burt",
        description="really good data",
        base_url="doi:10.5281/zenodo.6504891/",
        tomogram_metadata=tomogram_metadata,
    )

    # fields should be immutable
    with pytest.raises(TypeError):
        data_set.name = "new_name"
    with pytest.raises(TypeError):
        data_set.author = "new_author"
    with pytest.raises(TypeError):
        data_set.base_url = "new_url"
    with pytest.raises(TypeError):
        data_set.base_url = FileMetadata(
            file_name="new.zarr", checksum="123", reader=mrcfile.read
        )

    # repr and str should be the same
    assert str(data_set) == data_set._string_representation()
    assert str(data_set) == data_set.__repr__()


def test_data_set_from_dictionary():
    data_set = DataSet.from_dict(test_config_dict)
    assert isinstance(data_set, DataSet)


def test_data_set_invalid_name():
    """The DataSet name cannot have spaces"""
    tomogram_metadata = FileMetadata(
        file_name="01_10.00Apx.mrc",
        checksum="md5:426325d006fe04276ea01df9d83ad510",
        reader=mrcfile.read,
    )

    with pytest.raises(ValidationError):
        _ = DataSet(
            name=" hiv ",
            author="Alister Burt",
            description="really good data",
            base_url="doi:10.5281/zenodo.6504891/",
            tomogram_metadata=tomogram_metadata,
        )
