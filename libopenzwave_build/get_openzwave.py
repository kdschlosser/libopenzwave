# -*- coding: utf-8 -*-


import zipfile
import io
import os
from distutils import log as LOG  # NOQA

import libopenzwave_version


def get_openzwave(ozw_path, url):
    """download an archive to a specific location"""
    import requests

    LOG.info(
        "fetching {0} to {1} for version {2}".format(
            url,
            ozw_path,
            libopenzwave_version.ozw_version
        )
    )

    response = requests.get(url)
    dst_file = io.BytesIO(response.content)
    dst_file.seek(0)
    zip_ref = zipfile.ZipFile(dst_file)
    dst = os.path.split(ozw_path)[0]
    zip_ref.extractall(dst)
    zip_ref.close()
    dst_file.close()

    dst = os.path.join(dst, zip_ref.namelist()[0])

    if dst != ozw_path:
        os.rename(dst, ozw_path)
