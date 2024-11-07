#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLI definition for the filtering tool
"""
from eolab.rastertools import Filtering
#from eolab.rastertools.main import get_logger
from eolab.rastertools import RastertoolConfigurationException
#from eolab.rastertools.main import rastertools #Import the click group named rastertools
import logging
import sys
import click
import os

#TO DO
_logger = logging.getLogger("main")

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def _extract_files_from_list(cmd_inputs):
    """
    Extracts a list of file paths from a command line input.

    If the input is a single file with a `.lst` extension, it reads the file line-by-line and treats each
    line as an individual file path, returning the list of paths. If the input is already a
    list of file paths, it is returned as-is.

    Args:
        cmd_inputs (list of str):
            Command line inputs for file paths. If it contains a single `.lst` file, this file
            is read to obtain the list of files. Otherwise, it is assumed to be a direct list of files.

    Returns:
        list of str: A list of file paths, either extracted from the `.lst` file or passed directly.

    Example:
        _extract_files_from_list(["files.lst"])

        _extract_files_from_list(["file1.tif", "file2.tif"])

    Notes:
        The `.lst` file is expected to have one file path per line. Blank lines in the `.lst`
        file will be ignored.
    """
    # handle the input file of type "lst"
    if len(cmd_inputs) == 1 and cmd_inputs[0][-4:].lower() == ".lst":
        # parse the listing
        with open(cmd_inputs[0]) as f:
            inputs = f.read().splitlines()
    else:
        inputs = cmd_inputs

    return inputs

def create_filtering(output : str, window_size : int, pad : str, argsdict : dict, filter : str, bands : list, kernel_size : int, all_bands : bool) -> Filtering:
    """
    This function initializes a `Filtering` tool instance and configures it with specified settings.

    It selects the filter type, kernel size, output settings, and processing bands. If `all_bands` is set
    to True, the filter will apply to all bands in the raster; otherwise, it applies only to specified bands.

    Args:
        output (str): The path for the filtered output file.
        window_size (int): Size of the processing window used by the filter.
        pad (str): Padding method used for windowing (e.g., 'reflect', 'constant', etc.).
        argsdict (dict): Dictionary of additional filter configuration arguments.
        filter (str): The filter type to apply (must be a valid name in `Filtering` filters).
        bands (list): List of bands to process. If empty and `all_bands` is False, defaults to [1].
        kernel_size (int): Size of the kernel used by the filter.
        all_bands (bool): Whether to apply the filter to all bands (True) or specific bands (False).

    Returns:
        :obj:`eolab.rastertools.Filtering`: A configured `Filtering` instance ready for execution.
    """
    # get the bands to process
    if all_bands:
        bands = None
    else:
        bands = list(map(int, bands)) if bands else [1]

    # create the rastertool object
    raster_filters_dict = {rf.name: rf for rf in Filtering.get_default_filters()}
    tool = Filtering(raster_filters_dict[filter], kernel_size, bands)

    # set up config with args values
    tool.with_output(output) \
        .with_windows(window_size, pad) \
        .with_filter_configuration(argsdict)

    return tool


def apply_filter(ctx, tool : Filtering, inputs : str):
    """
    Apply the chosen filter to a set of input files.

    This function extracts input files, configures the filter tool, and processes the files
    through the specified filter. It also handles debug settings and intermediate file storage
    (VRT files). In case of any errors, the function logs the exception and terminates the process
    with an appropriate exit code.

    Args:
        ctx (click.Context): The context object containing configuration options like whether
                             to store intermediate VRT files.
        tool (Filtering): The `Filtering` tool instance that has been configured with the filter
                          and processing parameters.
        inputs (str): A path to a list of input files, either as a single `.lst` file or a direct
                      list of file paths. The list will be processed by the filter.

    Raises:
        RastertoolConfigurationException: If there is a configuration error with the tool.
        Exception: Any other errors that occur during processing.
    """
    try:
        # handle the input file of type "lst"
        inputs_extracted = _extract_files_from_list(inputs)

        # setup debug mode in which intermediate VRT files are stored to disk or not
        tool.with_vrt_stored(ctx.obj.get('keep_vrt'))

        # launch process
        tool.process_files(inputs_extracted)

        #_logger.info("Done!")

    except RastertoolConfigurationException as rce:
        #_logger.exception(rce)
        sys.exit(2)

    except Exception as err:
        #_logger.exception(err)
        sys.exit(1)

    sys.exit(0)


inpt_arg = click.argument('inputs', type=str, nargs = -1, required = 1)

ker_opt = click.option('--kernel_size', type=int, help="Kernel size of the filter function, e.g. 3 means a square" 
                   "of 3x3 pixels on which the filter function is computed"
                   "(default: 8)")

out_opt = click.option('-o', '--output', default = os.getcwd(), help="Output directory to store results (by default current directory)")

win_opt = click.option('-ws', '--window_size', type=int, default = 1024, help="Size of tiles to distribute processing, default: 1024")

pad_opt = click.option('-p','--pad',default="edge", type=click.Choice(['none','edge','maximum','mean','median','minimum','reflect','symmetric','wrap']),
              help="Pad to use around the image, default : edge" 
                  "(see https://numpy.org/doc/stable/reference/generated/numpy.pad.html"
                  "for more information)")

band_opt = click.option('-b','--bands', type=list, help="List of bands to process")

all_opt = click.option('-a', '--all','all_bands', type=bool, is_flag=True, help="Process all bands")

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def filter(ctx):
    """
    Apply a filter to a set of images.
    """
    ctx.ensure_object(dict)


def create_filter(filter_name : str):

    @filter.command(filter_name, context_settings=CONTEXT_SETTINGS)
    @inpt_arg
    @ker_opt
    @out_opt
    @win_opt
    @pad_opt
    @band_opt
    @all_opt
    @click.pass_context
    def filter_filtername(ctx, inputs : str, output : str, window_size : int, pad : str, kernel_size : int, bands : list, all_bands : bool):
        """
        Execute the requested filter on the input files with the specified parameters.
        The `inputs` argument can either be a single file or a `.lst` file containing a list of input files.

        Arguments:

        inputs TEXT

        Input file to process (e.g. Sentinel2 L2A MAJA from THEIA).
        You can provide a single file with extension \".lst\" (e.g. \"filtering.lst\") that lists
        the input files to process (one input file per line in .lst).
        """
        ctx.obj["inputs"] = inputs

        # Configure the filter tool instance
        tool = create_filtering(
            output=output,
            window_size=window_size,
            pad=pad,
            argsdict={"inputs": inputs},
            filter=filter_name,
            bands=bands,
            kernel_size=kernel_size,
            all_bands=all_bands)

        apply_filter(ctx, tool, inputs)


median = create_filter("median")
mean = create_filter("mean")
sum = create_filter("sum")
adaptive_gaussian = create_filter("adaptive_gaussian")

@filter.result_callback()
@click.pass_context
def handle_result(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()






