import mrcfile
import numpy as np

from cryo_et_sample_data._base import DataSet


def mrc_reader(file_path: str) -> np.ndarray:
    with mrcfile.open(file_path) as mrc:
        tomogram = mrc.data.copy()
    return tomogram


dataset_description = (
    "3D reconstruction of HIV virus-like particles from cryo-electron"
    "tomography data in EMPIAR-10164 and associated particle poses."
)

hiv_config = {
    "name": "hiv",
    "author": "Alister Burt",
    "description": dataset_description,
    "base_url": "doi:10.5281/zenodo.6504891/",
    "tomogram": {
        "file_name": "01_10.00Apx.mrc",
        "checksum": "md5:426325d006fe04276ea01df9d83ad510",
        "reader": mrc_reader,
    },
}

hiv = DataSet.from_dict(hiv_config)
