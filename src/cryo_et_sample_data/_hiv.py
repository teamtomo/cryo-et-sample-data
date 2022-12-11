"""Immature HIV-1 virus-like particle data from EMPIAR-10164.

This dataset contains a tomogram reconstructed from
data available in EMPIAR-10164.
"""

import mrcfile

from cryo_et_sample_data._data_set import DataSet

hiv_config = {
    "name": "hiv",
    "author": "Alister Burt",
    "description": __doc__,
    "base_url": "doi:10.5281/zenodo.6504891/",
    "tomogram_metadata": {
        "file_name": "01_10.00Apx.mrc",
        "checksum": "md5:426325d006fe04276ea01df9d83ad510",
        "reader": mrcfile.read,
    },
}

hiv = DataSet.from_dict(hiv_config)


def _hiv_sample_tomogram():
    """napari sample data function for hiv virus-like particles tomogram.

    Returns
    -------
    layer_data : List[LayerDataTuple]
        The data for the layers to be constructed.
        The LayerDataTuple has the following elements:
            - tomogram: the image
            - layer_kwargs: the keyword arguments passed to the
              napari add_image() method.
            - "image" the type of the layer
    """
    tomogram = hiv.tomogram

    # keyword arguments for Viewer.add_image()
    layer_kwargs = {"name": "HIV tomogram", "colormap": "gray_r"}

    return [(tomogram, layer_kwargs, "image")]
