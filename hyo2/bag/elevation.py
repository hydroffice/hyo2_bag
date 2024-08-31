import os
import logging

import numpy as np
from osgeo import gdal, osr

from hyo2.bag.meta import Meta
from hyo2.bag.helper import BAGError
from hyo2.bag.bag import BAGFile


logger = logging.getLogger(__name__)
gdal.UseExceptions()


class Elevation2Gdal:

    formats = {
        'ascii': ["AAIGrid", "bag.elevation.asc"],
        'geotiff': ["GTiff", "bag.elevation.tif"],
        'xyz': ["XYZ", "bag.elevation.xyz"],
    }

    def __init__(self, bag_elevation: np.ndarray, bag_meta: Meta, fmt="geotiff", out_file=None, epsg=None):
        """Export the elevation layer in one of the listed formats"""
        self.bag_elv = bag_elevation
        self.bag_meta = bag_meta

        # get the IN-MEMORY ogr driver
        self.mem = gdal.GetDriverByName("MEM")
        if self.mem is None:
            raise BAGError("%s driver not available.\n" % self.formats[fmt][0])
        logger.debug("format: %s" % fmt)

        # set the output file
        self.out_file = out_file
        if self.out_file is None:
            self.out_file = os.path.abspath(self.formats[fmt][1])
            logger.debug("output: %s" % self.out_file)

        if os.path.exists(self.out_file):
            os.remove(self.out_file)

        logger.debug("dtype: %s" % self.bag_elv.dtype)
        self.rst = self.mem.Create(utf8_path=self.out_file, xsize=self.bag_meta.cols, ysize=self.bag_meta.rows,
                                   bands=1, eType=gdal.GDT_Float32)
        # GDAL geo-transform refers to the top left corner of the top left pixel of the raster.
        self.rst.SetGeoTransform((self.bag_meta.sw[0] - self.bag_meta.res_x / 2.0, self.bag_meta.res_x, 0,
                                  self.bag_meta.ne[1] + self.bag_meta.res_y / 2.0, 0, -self.bag_meta.res_y))

        self.bnd = self.rst.GetRasterBand(1)
        self.bnd.WriteArray(self.bag_elv[::-1])
        self.bnd.SetNoDataValue(BAGFile.BAG_NAN)
        self.srs = osr.SpatialReference()
        if self.bag_meta.wkt_srs is not None:
            self.srs.ImportFromWkt(self.bag_meta.wkt_srs)
        else:
            logger.warning("unable to recover valid spatial reference info")
        if self.srs.IsCompound():
            self.srs.StripVertical()
        self.rst.SetProjection(self.srs.ExportToWkt())
        self.bnd.FlushCache()

        # get the required ogr driver
        self.drv = gdal.GetDriverByName(self.formats[fmt][0])

        # check if re-projection is required
        if not epsg:
            # if not, we just create a copy in the selected format
            _ = self.drv.CreateCopy(self.out_file, self.rst)
            _ = None
            self.rst = None
            return

        # we need to change projection:
        # - we create the output srs
        dst_srs = osr.SpatialReference()
        dst_srs.ImportFromEPSG(epsg)
        dst_wkt = dst_srs.ExportToWkt()

        # Call AutoCreateWarpedVRT() to fetch default values for target raster dimensions and geotransform
        tmp_ds = gdal.AutoCreateWarpedVRT(self.rst,
                                          None,  # src_wkt : left to default value --> will use the one from source
                                          dst_wkt,
                                          gdal.GRA_NearestNeighbour,
                                          0.125  # error threshold --> use same value as in gdalwarp
                                          )
        # Create the final warped raster
        _ = self.drv.CreateCopy(self.out_file, tmp_ds)
        _ = None
        self.rst = None
