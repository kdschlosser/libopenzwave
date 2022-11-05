# -*- coding: utf-8 -*-


import zipfile
import io
import os
import sys
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

    dst_file = io.BytesIO()
    dst_file.seek(0)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        content_length = int(r.headers['Content-Length'])
        chunks = 0
        print()
        sys.stdout.write('\r' + str(chunks) + '/' + str(content_length))
        sys.stdout.flush()

        for chunk in r.iter_content(chunk_size=1024):
            dst_file.write(chunk)
            chunks += len(chunk)
            sys.stdout.write('\r' + str(chunks) + '/' + str(content_length))
            sys.stdout.flush()

    zip_ref = zipfile.ZipFile(dst_file)
    dst = os.path.split(ozw_path)[0]
    zip_ref.extractall(dst)
    zip_ref.close()
    dst_file.close()

    dst = os.path.join(dst, zip_ref.namelist()[0])

    if dst != ozw_path:
        os.rename(dst, ozw_path)
