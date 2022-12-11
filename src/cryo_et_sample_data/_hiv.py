import mrcfile

from cryo_et_sample_data._data_set import DataSet

dataset_description = (
    "3D reconstruction of HIV virus-like particles from cryo-electron"
    " tomography data in EMPIAR-10164 and associated particle poses."
)

hiv_config = {
    "name": "hiv",
    "author": "Alister Burt",
    "description": dataset_description,
    "base_url": "doi:10.5281/zenodo.6504891/",
    "tomogram_metadata": {
        "file_name": "01_10.00Apx.mrc",
        "checksum": "md5:426325d006fe04276ea01df9d83ad510",
        "reader": mrcfile.read,
    },
}

hiv = DataSet.from_dict(hiv_config)
