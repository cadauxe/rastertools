#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the rastertools command line interface. The command line
has several subcommands such as *radioindice* and *zonalstats*.

Usage examples::

  rastertools radioindice --help
  rastertools zonalstats --help

"""
import logging
import logging.config
import os
import sys
import json
import click

from eolab.rastertools import __version__
from eolab.rastertools import RastertoolConfigurationException
from eolab.rastertools.cli import radioindice, zonalstats, tiling, speed
from eolab.rastertools.cli import filtering, svf, hillshade, timeseries
from eolab.rastertools.product import RasterType


_logger = logging.getLogger(__name__)

def add_custom_rastertypes(rastertypes):
    """Add definition of new raster types. The json string shall have the following format:

    .. code-block:: json

      {
        "rastertypes": [
          {
            "name": "RGB_TIF",
            "product_pattern": "^RGB_TIF_(?P<date>[0-9_]*)\\.(tif|TIF)$",
            "bands": [
              {
                "channel": "red",
                "description": "red"
              },
              {
                "channel": "green",
                "description": "green"
              },
              {
                "channel": "blue",
                "description": "blue"
              },
              {
                "channel": "nir",
                "description": "nir"
              }
            ],
            "date_format": "%Y%m%d_%H%M%S",
            "nodata": 0
          },
          {
            "name": "RGB_TIF_ARCHIVE",
            "product_pattern": "^RGB_TIF_(?P<date>[0-9\\_]*).*$",
            "bands_pattern": "^TIF_(?P<bands>{}).*\\.(tif|TIF)$",
            "bands": [
              {
                "channel": "red",
                "identifier": "r",
                "description": "red"
              },
              {
                "channel": "green",
                "identifier": "g",
                "description": "green"
              },
              {
                "channel": "blue",
                "identifier": "b",
                "description": "blue"
              },
              {
                "channel": "nir",
                "identifier": "n",
                "description": "nir"
              }
            ],
            "date_format": "%Y%m%d_%H%M%S",
            "nodata": 0
          }
        ]
      }

    - name : unique name of raster type
    - product_pattern: regexp to identify raster product matching the raster type. Regexp can
      contain catching groups that identifies metadata: date (groupe name=date), relative
      orbit number (relorbit), tile number (tile), any other group (free name of the group).
    - bands_pattern (optional) : when the raster product of this type is an archive
      (zip, tar, tar.gz, etc.), the pattern enables to identify the files of the different
      raster bands. The raster product can contain one raster file per band or one multi-bands
      raster file. In the first case, the pattern must contain a group that identify
      the band to which the file corresponds. This group must be defined as follows (?P<bands>{})
      in which the variable part {} will be replaced by the identifier of the band (see below).
    - date_format (optional): date format in the product name. By default: %Y%m%d-%H%M%S
    - nodata (optional): no data value of raster bands. By default: -10000
    - masknnodata (optional): nodata value in the mask band
    - For every bands:

      * channel: channel of the band. Must be one of: blue, green, red, nir, mir, swir,
        red_edge1, red_edge2, red_edge3, red_edge4, blue_60m, nir_60m and mir_60m.
      * identifier (optional): string that identifies the band in the filenames of a raster
        product that it is an archive. This identifier is inserted in the group ``bands`` of
        the bands_pattern.
      * description (optional): band description that will be reused in the generated products.

    - For every masks:

      * identifier (optional): string that identifies the mask band in the filenames of a raster
        product that it is an archive. This identifier is inserted in the group ``bands`` of
        the bands_pattern.
      * description (optional): mask band description that will be reused in the generated products.
      * maskfunc (optional): fully qualified name of the python function that converts the mask
        band values to a binary mask (0 = masked; 1 = unmasked)

    Args:
        rastertypes: JSON string that contains the new raster types definition
    """
    RasterType.add(rastertypes)

@click.group(help="Collection of tools on raster data.")

@click.option(
    '-t', '--rastertype',
    'rastertype',
    # Click automatically uses the last argument as the variable name, so "dest" is this last parameter
    type=click.Path(exists=True),
    help="JSON file defining additional raster types of input files")

@click.option(
    '--max_workers',
    "max_workers",
    type=int,
    help="Maximum number of workers for parallel processing. If not given, it will default to "
            "the number of processors on the machine. When all processors are not allocated to "
            "run rastertools, it is thus recommended to set this option.")

@click.option(
    '--debug',
    "keep_vrt",
    is_flag=True,
    help="Store to disk the intermediate VRT images that are generated when handling "
            "the input files which can be complex raster product composed of several band files.")

@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    help="set loglevel to INFO")

@click.option(
    '-vv',
    '--very-verbose',
    is_flag=True,
    help="set loglevel to DEBUG")

@click.version_option(version='rastertools {}'.format(__version__))  # Ensure __version__ is defined

def rastertools(rastertype, max_workers, keep_vrt, verbose, very_verbose, command, inputs):
    """
        CHANGE DOCSTRING
        Main entry point allowing external calls.

        Args:
            rastertype: JSON file defining additional raster types.
            max_workers: Maximum number of workers for parallel processing.
            debug: Store intermediate VRT images.
            verbose: Set loglevel to INFO.
            very_verbose: Set loglevel to DEBUG.
            command: The command to execute (e.g., filtering).
            inputs: Input files for processing.

        sys.exit returns:

        - 0: everything runs fine
        - 1: processing errors occured
        - 2: wrong execution configuration
    """
    # Setup logging
    if very_verbose:
        loglevel = logging.DEBUG
    elif verbose:
        loglevel = logging.INFO
    logformat = "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

    if "RASTERTOOLS_NOTQDM" not in os.environ:
        os.environ["RASTERTOOLS_NOTQDM"] = "True" if loglevel > logging.INFO else "False"

    if "RASTERTOOLS_MAXWORKERS" not in os.environ and max_workers is not None:
        os.environ["RASTERTOOLS_MAXWORKERS"] = f"{max_workers}"

    # Handle rastertype option
    if rastertype:
        with open(rastertype) as json_content:
            RasterType.add(json.load(json_content))

    # Map command string to function
    command_mapping = {
        'filtering': filtering.command,
        'hillshade': hillshade.command,
        'radioindice': radioindice.command,
        'speed': speed.command,
        'svf': svf.command,
        'tiling': tiling.command,
        'timeseries': timeseries.command,
        'zonalstats': zonalstats.command,
    }

    tool = command_mapping.get(command)

    # Call the corresponding function for the specified command

    if tool:
        try:
            # handle the input file of type "lst"
            inputs_extracted = _extract_files_from_list(inputs)

            # setup debug mode in which intermediate VRT files are stored to disk or not
            tool.with_vrt_stored(keep_vrt)

            # launch process
            tool.process_files(inputs_extracted)

            _logger.info("Done!")

        except RastertoolConfigurationException as rce:
            _logger.exception(rce)
            sys.exit(2)

        except Exception as err:
            _logger.exception(err)
            sys.exit(1)
    else:
        ctx.show_help()

    sys.exit(0)


# Register subcommands from other modules
rastertools.add_command(filtering.filter, "filter")
rastertools.add_command(hillshade.command, "hillshade")
rastertools.add_command(radioindice.command, "radioindice")
rastertools.add_command(speed.command, "speed")
rastertools.add_command(svf.command, "svf")
rastertools.add_command(tiling.command, "tiling")
rastertools.add_command(timeseries.command, "timeseries")
rastertools.add_command(zonalstats.command, "zonalstats")


def _extract_files_from_list(cmd_inputs):
    """Extract the list of files from a file of type ".lst" which
    contains one line per file

    Args:
        cmd_inputs (str):
            Value of the inputs arguments of the command line. Either
            a file with a suffix lst from which the list of files shall
            be extracted or directly the list of files (in this case, the
            list is returned without any change).

    Returns:
        The list of input files read from the command line
    """

    # handle the input file of type "lst"
    if len(cmd_inputs) == 1 and cmd_inputs[0][-4:].lower() == ".lst":
        # parse the listing
        with open(cmd_inputs[0]) as f:
            inputs = f.read().splitlines()
    else:
        inputs = cmd_inputs

    return inputs


def run():
    """Entry point for console_scripts
    """
    rastertools()


if __name__ == "__main__":
    run()
