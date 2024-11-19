# -*- coding: utf-8 -*-
"""
    Setup file for rastertools.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.0.2.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
# import os
# import logging
# from subprocess import check_output
# import sys
#
# import re
# import shutil
from setuptools import setup, find_packages
# from sphinx.builders.html import setup_resource_paths

# with open('src/eolab/rastertools/__init__.py') as f:
#     for line in f:
#         if line.find("__version__") >= 0:
#             version = line.split("=")[1].strip()
#             version = version.strip('"')
#             version = version.strip("'")
#             break


# logging.basicConfig(stream=sys.stderr, level=logging.INFO)
# log = logging.getLogger()
#
# # options will need to be set in setup.cfg or on the setup command line.
# include_dirs = []
# library_dirs = []
# libraries = []
# extra_link_args = []
# gdal2plus = False
# gdal_output = [None] * 4
# gdalversion = None
# gdal_major_version = 0
# gdal_minor_version = 0
# gdal_patch_version = 0
#
#
# def copy_data_tree(datadir, destdir):
#     try:
#         shutil.rmtree(destdir)
#     except OSError:
#         pass
#     shutil.copytree(datadir, destdir)
#
# if "clean" not in sys.argv:
#     try:
#         gdal_config = os.environ.get('GDAL_CONFIG', 'gdal-config')
#         for i, flag in enumerate(("--cflags", "--libs", "--datadir", "--version")):
#             gdal_output[i] = check_output([gdal_config, flag]).decode("utf-8").strip()
#
#         for item in gdal_output[0].split():
#             if item.startswith("-I"):
#                 include_dirs.extend(item[2:].split(":"))
#         for item in gdal_output[1].split():
#             if item.startswith("-L"):
#                 library_dirs.extend(item[2:].split(":"))
#             elif item.startswith("-l"):
#                 libraries.append(item[2:])
#             else:
#                 # e.g. -framework GDAL
#                 extra_link_args.append(item)
#         # datadir, gdal_output[2] handled below
#
#         gdalversion = gdal_output[3]
#         if gdalversion:
#             log.info("GDAL API version obtained from gdal-config: %s",
#                      gdalversion)
#
#     except Exception as e:
#         if os.name == "nt":
#             log.info("Building on Windows requires extra options to setup.py "
#                      "to locate needed GDAL files. More information is available "
#                      "in the README.")
#         else:
#             log.warning("Failed to get options via gdal-config: %s", str(e))
#
#     # Get GDAL API version from environment variable.
#     if 'GDAL_VERSION' in os.environ:
#         gdalversion = os.environ['GDAL_VERSION']
#         log.info("GDAL API version obtained from environment: %s", gdalversion)
#
#     # Get GDAL API version from the command line if specified there.
#     if '--gdalversion' in sys.argv:
#         index = sys.argv.index('--gdalversion')
#         sys.argv.pop(index)
#         gdalversion = sys.argv.pop(index)
#         log.info("GDAL API version obtained from command line option: %s",
#                  gdalversion)
#
#     if not gdalversion:
#         raise SystemExit("ERROR: A GDAL API version must be specified. Provide a path "
#                  "to gdal-config using a GDAL_CONFIG environment variable "
#                  "or use a GDAL_VERSION environment variable.")
#
#     gdal_major_version, gdal_minor_version, gdal_patch_version = map(
#         int, re.findall("[0-9]+", gdalversion)[:3]
#     )
#
#     if (gdal_major_version, gdal_minor_version) < (3, 5):
#         raise SystemExit("ERROR: GDAL >= 3.5 is required for rasterio. "
#                  "Please upgrade GDAL.")
#
# # Conditionally copy the GDAL data. To be used in conjunction with
# # the bdist_wheel command to make self-contained binary wheels.
# if os.environ.get('PACKAGE_DATA'):
#     destdir = 'rasterio/gdal_data'
#     if gdal_output[2]:
#         log.info("Copying gdal data from %s" % gdal_output[2])
#         copy_data_tree(gdal_output[2], destdir)
#     else:
#         # check to see if GDAL_DATA is defined
#         gdal_data = os.environ.get('GDAL_DATA', None)
#         if gdal_data:
#             log.info("Copying gdal_data from %s" % gdal_data)
#             copy_data_tree(gdal_data, destdir)
#
#     # Conditionally copy PROJ DATA.
#     projdatadir = os.environ.get('PROJ_DATA', os.environ.get('PROJ_LIB', '/usr/local/share/proj'))
#     if os.path.exists(projdatadir):
#         log.info("Copying proj_data from %s" % projdatadir)
#         copy_data_tree(projdatadir, 'rasterio/proj_data')


if __name__ == "__main__":
    try:
        setup(name='rastertools',
              version="0.1.0",
              description=u"Collection of tools for raster data",
              long_description="",
              classifiers=[],
              keywords='',
              author=u"Olivier Queyrut",
              author_email="",
              url="https://github.com/CNES/rastertools",
              packages=find_packages(exclude=['tests']),
              include_package_data=True,
              zip_safe=False,
              setup_requires = ["setuptools_scm"],
              install_requires=[
                  'click',
                  'rasterio==1.3.0',
                  'pytest>=3.6',
                  'pytest-cov',
                  'geopandas==0.13',
                  'python-dateutil==2.9.0',
                  'kiwisolver==1.4.5',
                  'fonttools==4.53.1',
                  'matplotlib==3.7.3',
                  'packaging==24.1',
                  'Shapely==1.8.5.post1',
                  'tomli==2.0.2',
                  'Rtree==1.3.0',
                  'Pillow==9.2.0',
                  'pip==24.2',
                  'pyproj==3.4.0',
                  'matplotlib',
                  'scipy==1.8',
                  'pyscaffold',
                  # 'gdal==3.5.0',
                  'tqdm==4.66'
              ],
              # extras_require={
              #     "gdal": ["gdal>=3.0.0,<4.0.0"],
              # },
              entry_points="""[rasterio.plugins]
              rastertools=src.eolab.rastertools.main:rastertools""",
              python_requires='==3.8.13',
              use_scm_version={"version_scheme": "no-guess-dev"})
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
