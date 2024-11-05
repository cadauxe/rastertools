#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLI definition for the filtering tool
"""
import eolab.rastertools.cli as cli
from eolab.rastertools import Filtering
import click
import os

def create_filtering(output : str, window_size : int, pad : str, filter : str, bands : list, kernel_size : int, all : bool) -> Filtering:
    """
    CHANGE DOCSTRING
    Create and configure a new rastertool "Filtering" according to argparse args

    Args:
        args: args extracted from command line

    Returns:
        :obj:`eolab.rastertools.Filtering`: The configured rastertool to run
    """

    # get the bands to process
    if all:
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


@click.group(help="Apply a filter to a set of images.")
def filter():
    pass

#Median filter
@filter.command("median")
@click.argument('inputs', type=str, help="Input file to process (e.g. Sentinel2 L2A MAJA from THEIA). "
                 "You can provide a single file with extension \".lst\" (e.g. \"filtering.lst\") "
                 "that lists the input files to process (one input file per line in .lst)")

@click.option('--kernel-size', type=int,
              help="Kernel size of the filter function, e.g. 3 means a square" 
                   "of 3x3 pixels on which the filter function is computed"
                   "(default: 8)")

@click.option('-o', '--output', default = os.getcwd(), help="Output directory to store results (by default current directory)")

@click.option('-ws', '--window-size', type=int, default = 1024, help="Size of tiles to distribute processing, default: 1024")

@click.option('-p','--pad',default="edge", type=click.Choice(['none','edge','maximum','mean','median','minimum','reflect','symmetric','wrap']),
              help="Pad to use around the image, default : edge" 
                  "(see https://numpy.org/doc/stable/reference/generated/numpy.pad.html"
                  "for more information)")

@click.option('-b','--bands', type=list, help="List of bands to process")

@click.option('-a', '--all','all_bands', type=bool, is_flag=True, help="Process all bands")

def median(inputs : str, output : str, window_size : int, pad : str, kernel_size : int, bands : list, all_bands : str):
    """
    COMPLETE THE SECTION should display for : rastertools filter median --help
    Execute the filtering tool with the specified filter and parameters. name=rasterfilter.name, help=rasterfilter.help
    """
    # Configure the filter tool instance
    tool = create_filtering(
            output=output,
            window_size=window_size,
            pad=pad,
            argsdict={"inputs": inputs},
            filter='median',
            bands=bands,
            kernel_size=kernel_size,
            all_bands=all_bands)

    # Process the input files
    ##tool.process_files(inputs) suppr?

#Sum filter
@filter.command("sum")
@click.argument('inputs', type=str, help="Input file to process (e.g. Sentinel2 L2A MAJA from THEIA). "
                 "You can provide a single file with extension \".lst\" (e.g. \"filtering.lst\") "
                 "that lists the input files to process (one input file per line in .lst)")

@click.option('--kernel-size', type=int,
              help="Kernel size of the filter function, e.g. 3 means a square" 
                   "of 3x3 pixels on which the filter function is computed"
                   "(default: 8)")

@click.option('-o', '--output', default = os.getcwd(), help="Output directory to store results (by default current directory)")

@click.option('-ws', '--window-size', type=int, default = 1024, help="Size of tiles to distribute processing, default: 1024")

@click.option('-p','--pad',default="edge", type=click.Choice(['none','edge','maximum','mean','median','minimum','reflect','symmetric','wrap']),
              help="Pad to use around the image, default : edge" 
                  "(see https://numpy.org/doc/stable/reference/generated/numpy.pad.html"
                  "for more information)")

@click.option('-b','--bands', type=list, help="List of bands to process")

@click.option('-a', '--all','all_bands', type=bool, is_flag=True, help="Process all bands")

def sum(inputs : str, output : str, window_size : int, pad : str, kernel_size : int, bands : list, all_bands : str):
    """
    COMPLETE THE SECTION should display for : rastertools filter median --help
    Execute the filtering tool with the specified filter and parameters. name=rasterfilter.name, help=rasterfilter.help
    """
    # Configure the filter tool instance
    tool = create_filtering(
            output=output,
            window_size=window_size,
            pad=pad,
            argsdict={"inputs": inputs},
            filter='sum',
            bands=bands,
            kernel_size=kernel_size,
            all_bands=all_bands)

#Mean filter
@filter.command("mean")
@click.argument('inputs', type=str, help="Input file to process (e.g. Sentinel2 L2A MAJA from THEIA). "
                 "You can provide a single file with extension \".lst\" (e.g. \"filtering.lst\") "
                 "that lists the input files to process (one input file per line in .lst)")

@click.option('--kernel-size', type=int,
              help="Kernel size of the filter function, e.g. 3 means a square" 
                   "of 3x3 pixels on which the filter function is computed"
                   "(default: 8)")

@click.option('-o', '--output', default = os.getcwd(), help="Output directory to store results (by default current directory)")

@click.option('-ws', '--window-size', type=int, default = 1024, help="Size of tiles to distribute processing, default: 1024")

@click.option('-p','--pad',default="edge", type=click.Choice(['none','edge','maximum','mean','median','minimum','reflect','symmetric','wrap']),
              help="Pad to use around the image, default : edge" 
                  "(see https://numpy.org/doc/stable/reference/generated/numpy.pad.html"
                  "for more information)")

@click.option('-b','--bands', type=list, help="List of bands to process")

@click.option('-a', '--all','all_bands', type=bool, is_flag=True, help="Process all bands")

def mean(inputs : str, output : str, window_size : int, pad : str, kernel_size : int, bands : list, all_bands : str):
    """
    COMPLETE THE SECTION should display for : rastertools filter median --help
    Execute the filtering tool with the specified filter and parameters. name=rasterfilter.name, help=rasterfilter.help
    """
    # Configure the filter tool instance
    tool = create_filtering(
            output=output,
            window_size=window_size,
            pad=pad,
            argsdict={"inputs": inputs},
            filter='mean',
            bands=bands,
            kernel_size=kernel_size,
            all_bands=all_bands)

#Adaptive gaussian filter
@filter.command("adaptive_gaussian")
@click.argument('inputs', type=str, help="Input file to process (e.g. Sentinel2 L2A MAJA from THEIA). "
                 "You can provide a single file with extension \".lst\" (e.g. \"filtering.lst\") "
                 "that lists the input files to process (one input file per line in .lst)")

@click.option('--kernel-size', type=int,
              help="Kernel size of the filter function, e.g. 3 means a square" 
                   "of 3x3 pixels on which the filter function is computed"
                   "(default: 8)")

@click.option('-o', '--output', default = os.getcwd(), help="Output directory to store results (by default current directory)")

@click.option('-ws', '--window-size', type=int, default = 1024, help="Size of tiles to distribute processing, default: 1024")

@click.option('-p','--pad',default="edge", type=click.Choice(['none','edge','maximum','mean','median','minimum','reflect','symmetric','wrap']),
              help="Pad to use around the image, default : edge" 
                  "(see https://numpy.org/doc/stable/reference/generated/numpy.pad.html"
                  "for more information)")

@click.option('-b','--bands', type=list, help="List of bands to process")

@click.option('-a', '--all','all_bands', type=bool, is_flag=True, help="Process all bands")

def adaptive_gaussian(inputs : str, output : str, window_size : int, pad : str, kernel_size : int, bands : list, all_bands : str):
    """
    COMPLETE THE SECTION should display for : rastertools filter median --help
    Execute the filtering tool with the specified filter and parameters. name=rasterfilter.name, help=rasterfilter.help
    """
    # Configure the filter tool instance
    tool = create_filtering(
            output=output,
            window_size=window_size,
            pad=pad,
            argsdict={"inputs": inputs},
            filter='adaptive_gaussian',
            bands=bands,
            kernel_size=kernel_size,
            all_bands=all_bands)








