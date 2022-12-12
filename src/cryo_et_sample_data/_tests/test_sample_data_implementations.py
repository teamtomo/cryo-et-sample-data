import pytest

from cryo_et_sample_data._hiv import _hiv_sample_tomogram
from cryo_et_sample_data._tests.utils import on_ci


@pytest.mark.skipif(on_ci, reason="data too big to download on CI")
def test_hiv_sample_tomogram():
    sample_data = _hiv_sample_tomogram()

    # there should be one layer
    assert isinstance(sample_data, list)
    assert len(sample_data) == 1

    layer_data_tuple = sample_data[0]
    assert len(layer_data_tuple) == 3
    assert isinstance(layer_data_tuple, tuple)
    assert isinstance(layer_data_tuple[1], dict)
    assert layer_data_tuple[2] == "image"
