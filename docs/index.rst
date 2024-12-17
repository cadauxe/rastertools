============
georastertools
============

This project consists in a command line named **georastertools** that enables to run several processing on raster files, typically
Sentinel2 raster images:

- compute radiometric indices (e.g. ndvi).
- compute the time derivative of the radiometry of two raster images.
- generate a timeseries of rasters from a set of input rasters; a linear interpolation and a gap
  filling are performed.
- compute statistics such as min, max, mean, etc. Statistics can be computed on the whole raster image
  or can be computed on several geometries defined with a vector file - e.g. geojson or shapefile.
- split input image raster in tiles following the geometries defined in a vector file.
- apply a filter (median, local sum, local mean, adaptive gaussian)
- compute the Sky View Factor and the Hillshades of input rasters that represent a Digital Surface/Elevation/Height Model.

The aim of **georastertools** is also to make the use of the following raster products transparent:

- Sentinel-2 L1C PEPS (available here: https://peps.cnes.fr/rocket/#/search)
- Sentinel-2 L2A PEPS (available here: https://peps.cnes.fr/rocket/#/search)
- Sentinel-2 L2A THEIA (available here: https://theia.cnes.fr/atdistrib/rocket/#/search?collection=SENTINEL2)
- Sentinel-2 L3A THEIA (available here: https://theia.cnes.fr/atdistrib/rocket/#/search?collection=SENTINEL2)
- SPOT 6/7 Ortho GEOSUD (available here: http://ids.equipex-geosud.fr/web/guest/catalog)

**georastertools** accept any of this raster product as input files. No need to unpack the archive to get
the raster files containing the different bands, to merge the bands, extract the region of interest and
so on: **georastertools** does it.

**georastertools** also accepts additional custom raster types. The new raster types shall be defined in a
JSON file and provided as an argument of the georastertools CLI (cf. Usage)

**georastertools** has a public API that enables to activate all the tools and extend their capabilities (e.g.
add a new radiometric indice).


Contents
========

**Install**

* :doc:`install`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Installation

   install


**Usage**

* :doc:`cli`
* :doc:`usage`
* :doc:`rasterproduct`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Usage

   cli
   usage
   rasterproduct

**Development**

* :doc:`private_api`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Development

   private_api

**About**

* :doc:`license`
* :doc:`authors`
* :doc:`changelog`

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: About

   license
   authors
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _theia: https://theia.cnes.fr/atdistrib/rocket/#/search?collection=SENTINEL2
.. _peps: https://peps.cnes.fr/rocket/#/search
.. _geosud: http://ids.equipex-geosud.fr/web/guest/catalog
.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
