# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

if __name__ == "__main__":
    try:
        with open("README.rst", "r", encoding="utf-8") as fh:
            long_description = fh.read()

        setup(name='georastertools',
              version="0.1.0",
              description="Collection of tools for raster data",
              long_description=long_description,
              long_description_content_type="text/x-rst",
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
                  'rasterio',
                  'pytest>=3.6',
                  'pytest-cov',
                  'geopandas==0.13',
                  'kiwisolver==1.4.5',
                  'matplotlib==3.7.3',
                  'packaging==24.1',
                  'fiona==1.8.21',
                  'sphinx_rtd_theme==3.0.1',
                  'pip==24.2',
                  'sphinx==7.1.2',
                  'scipy==1.8',
                  'pyscaffold',
                  'gdal==3.5.0',
                  'tqdm==4.66'
              ],
              entry_points="""
                [rasterio.rio_plugins]
                georastertools=eolab.georastertools.main:georastertools
                """,
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
