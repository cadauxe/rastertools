#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import filecmp
import zipfile
from pathlib import Path
from datetime import datetime

import rasterio

from eolab.rastertools.product import RasterType, BandChannel
from eolab.rastertools.product import RasterProduct

from . import utils4test

__author__ = "Olivier Queyrut"
__copyright__ = "Copyright 2019, CNES"
__license__ = "Apache v2.0"


__refdir = utils4test.get_refdir("test_rasterproduct/")


def test_rasterproduct_valid_parameters():
    # archive with one file per band
    basename = "S2B_MSIL1C_20191008T105029_N0208_R051_T30TYP_20191008T125041"
    file = Path(
        utils4test.indir + basename + ".zip")
    prod = RasterProduct(file)

    assert prod.file == file
    assert prod.rastertype == RasterType.get("S2_L1C")
    assert prod.channels == RasterType.get("S2_L1C").channels
    band_format = f"/vsizip/tests/tests_data/{basename}.zip/"
    band_format += f"{basename}.SAFE/GRANULE/L1C_T30TYP_A013519_20191008T105335/IMG_DATA/"
    band_format += "T30TYP_20191008T105029_{}.jp2"
    assert prod.bands_files == {b: band_format.format(b) for b in prod.rastertype.get_band_ids()}
    assert prod.masks_files == {}
    assert prod.is_archive
    assert prod.get_date() == datetime(2019, 10, 8, 10, 50, 29)
    assert prod.get_date_string('%Y%m%d-%H%M%S') == "20191008-105029"
    assert prod.get_tile() == "30TYP"
    assert prod.get_relative_orbit() == 51
    assert prod.get_satellite() == "S2B"

    # archive with one file for all bands
    basename = "SPOT6_2018_France-Ortho_NC_DRS-MS_SPOT6_2018_FRANCE_ORTHO_NC_GEOSUD_MS_82"
    file = utils4test.indir + basename + ".tar.gz"
    prod = RasterProduct(file)

    assert prod.file == Path(file)
    assert prod.rastertype == RasterType.get("SPOT67_GEOSUD")
    assert prod.channels == [BandChannel.red, BandChannel.green, BandChannel.blue, BandChannel.nir]
    band = f"/vsitar/tests/tests_data/{basename}.tar.gz/SPOT6_2018_FRANCE_ORTHO_NC_GEOSUD_MS_82/"
    band += "PROD_SPOT6_001/VOL_SPOT6_001_A/IMG_SPOT6_MS_001_A/"
    band += "IMG_SPOT6_MS_201805111031189_ORT_SPOT6_20180517_1333011n1b80qobn5ex_1_R1C1.TIF"
    assert prod.bands_files == {"all": band}
    assert prod.masks_files == {}
    assert prod.is_archive
    assert prod.get_date() is None
    assert prod.get_date_string() == ""
    assert prod.get_tile() is None
    assert prod.get_relative_orbit() is None
    assert prod.get_satellite() == "SPOT6"

    # regular raster file
    basename = "RGB_TIF_20170105_013442_test.tif"
    file = utils4test.indir + basename
    prod = RasterProduct(file)

    assert prod.file == Path(file)
    assert prod.rastertype is None
    assert prod.channels == []
    assert prod.bands_files == {"all": Path(file).as_posix()}
    assert prod.masks_files == {}
    assert prod.is_archive is False
    assert prod.get_date() is None
    assert prod.get_date_string('%Y%m%d-%H%M%S') == ""
    assert prod.get_tile() is None
    assert prod.get_relative_orbit() is None
    assert prod.get_satellite() is None


def test_rasterproduct_invalid_parameters():
    with pytest.raises(ValueError) as exc:
        RasterProduct(None)
    assert "'file' cannot be None" in str(exc.value)

    file = utils4test.indir + "InvalidName.zip"
    with pytest.raises(ValueError) as exc:
        RasterProduct(file)
    assert f"Unrecognized raster type for input file {file}" in str(exc.value)

    file = utils4test.indir + "grid.geojson"
    with pytest.raises(ValueError) as exc:
        RasterProduct(file)
    assert f"Unsupported input file {file}" in str(exc.value)


def test_create_product_S2_L2A_MAJA(compare, save_gen_as_ref):
    # create output dir and clear its content if any
    utils4test.create_outdir()

    # unzip SENTINEL2B_20181023-105107-455_L2A_T30TYP_D.zip
    file = utils4test.indir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D.zip"
    with zipfile.ZipFile(file) as myzip:
        myzip.extractall(utils4test.outdir)

    # creation of S2 L2A MAJA products
    files = [Path(utils4test.indir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D.zip"),
             Path(utils4test.indir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D_tar.tar"),
             Path(utils4test.indir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D_targz.TAR.GZ"),
             Path(utils4test.outdir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D_V1-9")]

    for file in files:
        with RasterProduct(file, vrt_outputdir=Path(utils4test.outdir)) as prod:
            raster = prod.get_raster(roi=Path(utils4test.indir + "COMMUNE_32001.shp"),
                                     masks="all")

            assert Path(raster).exists()
            assert raster == utils4test.outdir + utils4test.basename(file) + "-mask.vrt"

            ref = [utils4test.basename(file) + ".vrt",
                   utils4test.basename(file) + "-clipped.vrt",
                   utils4test.basename(file) + "-mask.vrt"]

            if compare:
                print(f"compare {utils4test.outdir} ,{__refdir}, {ref}")
                match, mismatch, err = utils4test.cmpfiles(utils4test.outdir, __refdir, ref)
                assert len(match) == len(ref)
                assert len(mismatch) == 0
                assert len(err) == 0
            elif save_gen_as_ref:
                # save the generated files in the refdir => make them the new refs.
                utils4test.copy_to_ref(ref, __refdir)

            # check if product can be opened by rasterio
            dataset = rasterio.open(raster)
            dataset.close()

        utils4test.clear_outdir(subdirs=False)

    # delete the dir resulting from unzip
    utils4test.delete_dir(utils4test.outdir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D_V1-9")


def test_create_product_S2_L1C(compare, save_gen_as_ref):
    # create output dir and clear its content if any
    utils4test.create_outdir()

    # creation of S2 L1C product
    infile = utils4test.indir + "S2B_MSIL1C_20191008T105029_N0208_R051_T30TYP_20191008T125041.zip"

    with RasterProduct(infile, vrt_outputdir=utils4test.outdir) as prod:
        raster = prod.get_raster(roi=utils4test.indir + "/COMMUNE_32001.shp",
                                 masks="all")
        assert Path(raster).exists()
        assert raster == utils4test.outdir + utils4test.basename(infile) + "-clipped.vrt"

        gen_files = [utils4test.basename(infile) + ".vrt",
                     utils4test.basename(infile) + "-clipped.vrt"]
        if compare:
            match, mismatch, err = utils4test.cmpfiles(utils4test.outdir, __refdir, gen_files)
            assert len(match) == 2
            assert len(mismatch) == 0
            assert len(err) == 0
        elif save_gen_as_ref:
            # save the generated files in the refdir => make them the new refs.
            utils4test.copy_to_ref(gen_files, __refdir)

        # check if product can be opened by rasterio
        dataset = rasterio.open(raster)
        dataset.close()

    utils4test.clear_outdir()


def test_create_product_S2_L2A_SEN2CORE(compare, save_gen_as_ref):
    # create output dir and clear its content if any
    utils4test.create_outdir()

    # creation of S2 L2A SEN2CORE product
    infile = utils4test.indir + "S2A_MSIL2A_20190116T105401_N0211_R051_T30TYP_20190116T120806.zip"
    with RasterProduct(infile, vrt_outputdir=utils4test.outdir) as prod:
        raster = prod.get_raster()

        assert Path(raster).exists()
        assert raster == utils4test.outdir + utils4test.basename(infile) + ".vrt"

        gen_files = [utils4test.basename(infile) + ".vrt"]
        if compare:
            match, mismatch, err = utils4test.cmpfiles(utils4test.outdir, __refdir, gen_files)
            assert len(match) == 1
            assert len(mismatch) == 0
            assert len(err) == 0
        elif save_gen_as_ref:
            # save the generated files in the refdir => make them the new refs.
            utils4test.copy_to_ref(gen_files, __refdir)

        # check if product can be opened by rasterio
        dataset = rasterio.open(raster)
        dataset.close()

    utils4test.clear_outdir()


def test_create_product_SPOT67(compare, save_gen_as_ref):
    # create output dir and clear its content if any
    utils4test.create_outdir()

    # creation of SPOT67 product
    infile = "SPOT6_2018_France-Ortho_NC_DRS-MS_SPOT6_2018_FRANCE_ORTHO_NC_GEOSUD_MS_82.tar.gz"
    with RasterProduct(utils4test.indir + infile, vrt_outputdir=utils4test.outdir) as prod:
        raster = prod.get_raster()

        assert Path(raster).exists()
        assert raster == utils4test.outdir + utils4test.basename(infile) + ".vrt"

        gen_files = [utils4test.basename(infile) + ".vrt"]
        if compare:
            match, mismatch, err = utils4test.cmpfiles(utils4test.outdir, __refdir, gen_files)
            assert len(match) == 1
            assert len(mismatch) == 0
            assert len(err) == 0
        elif save_gen_as_ref:
            # save the generated files in the refdir => make them the new refs.
            utils4test.copy_to_ref(gen_files, __refdir)

        # check if product can be opened by rasterio
        dataset = rasterio.open(raster)
        dataset.close()

    utils4test.clear_outdir()


def test_create_product_special_cases():
    # SUPPORTED CASES

    # creation in memory (without masks)
    file = "S2B_MSIL1C_20191008T105029_N0208_R051_T30TYP_20191008T125041.zip"
    with RasterProduct(utils4test.indir + file) as prod:
        assert prod.get_raster(masks=None).endswith(utils4test.basename(file) + ".vrt")
        # check if product can be opened by rasterio
        dataset = prod.open()
        dataset.close()

    # creation in memory (with masks)
    file = "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D_tar.tar"
    with RasterProduct(utils4test.indir + file) as prod:
        raster = prod.get_raster(roi=Path(utils4test.indir + "COMMUNE_32001.shp"),
                                 bands=prod.rastertype.get_band_ids(),
                                 masks=prod.rastertype.get_mask_ids())

        assert raster.endswith(utils4test.basename(file) + "-mask.vrt")

        # check if product can be opened by rasterio
        with rasterio.Env(GDAL_VRT_ENABLE_PYTHON=True):
            with rasterio.open(raster) as dataset:
                data = dataset.read([1], masked=True)
                # pixel corresponding to a value > 0 for a band mask => masked value
                assert data.mask[0][350][250]

    # creation from a vrt
    file = "S2A_MSIL2A_20190116T105401_N0211_R051_T30TYP_20190116T120806.vrt"
    with RasterProduct(utils4test.indir + file) as prod:
        raster = prod.get_raster()
        assert raster == utils4test.indir + utils4test.basename(file) + ".vrt"
        assert prod.rastertype == RasterType.get("S2_L2A_SEN2CORE")
        # check if product can be opened by rasterio
        dataset = rasterio.open(raster)
        dataset.close()

    # creation from a directory
    # unzip S2B_MSIL1C_20191008T105029_N0208_R051_T30TYP_20191008T125041.zip
    file = utils4test.indir + "S2B_MSIL1C_20191008T105029_N0208_R051_T30TYP_20191008T125041.zip"
    with zipfile.ZipFile(file) as myzip:
        myzip.extractall(utils4test.outdir)
    dirname = "S2B_MSIL1C_20191008T105029_N0208_R051_T30TYP_20191008T125041.SAFE"

    with RasterProduct(file, vrt_outputdir=Path(utils4test.outdir)) as prod:
        raster = prod.get_raster()
        assert raster == utils4test.outdir + utils4test.basename(file) + ".vrt"
        # check if product can be opened by rasterio
        dataset = rasterio.open(raster)
        dataset.close()

    # ERROR CASES

    # creation of a product with bands that do not exist in corresponding rastertype
    # file = "SPOT6_2018_France-Ortho_NC_DRS-MS_SPOT6_2018_FRANCE_ORTHO_NC_GEOSUD_MS_82.tar.gz"
    # channels = [BandChannel.red, BandChannel.green, BandChannel.blue, BandChannel.swir]
    # with pytest.raises(ValueError) as exc:
    #     prod = RasterProduct(utils4test.indir + file,
    #                                         RasterType.get("SPOT67_GEOSUD"),
    #                                         channels)
    # msg = f"RasterType does not contain all the channels in {channels}"
    # assert msg in str(exc.value)

    # creation of a product with bands that do not exist in the product (but that
    # do exist in rastertype)
    file = utils4test.indir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D.zip"
    with zipfile.ZipFile(file) as myzip:
        names = myzip.namelist()
        selection = []
        for n in names:
            if n.endswith("FRE_B2.tif") or \
               n.endswith("FRE_B3.tif") or \
               n.endswith("FRE_B4.tif") or \
               n.endswith("CLM_R1.tif"):
                selection.append(n)
        myzip.extractall(utils4test.outdir, selection)

    file = Path(utils4test.outdir + "SENTINEL2B_20181023-105107-455_L2A_T30TYP_D_V1-9")

    with pytest.raises(ValueError) as exc:
        prod = RasterProduct(file)
        prod.get_raster(bands=prod.rastertype.get_band_ids())
    msg = f"Invalid band id FRE_B8: it does not exist in raster product"
    assert msg in str(exc.value)

    with pytest.raises(ValueError) as exc:
        prod = RasterProduct(file)
        prod.get_raster(masks=prod.rastertype.get_mask_ids())
    msg = f"Invalid mask id SAT_R1: it does not exist in raster product"
    assert msg in str(exc.value)

    with pytest.raises(ValueError) as exc:
        prod = RasterProduct(file)
        prod.get_raster(bands=None)
    msg = "Invalid bands list: must be 'all' or a valid no empty list of band ids"
    assert msg in str(exc.value)

    utils4test.clear_outdir()
