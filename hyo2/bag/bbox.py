import os
import logging

from osgeo import ogr, osr
from hyo2.bag.meta import Meta
from hyo2.bag.helper import BAGError, Helper
from hyo2.bag import __version__


logger = logging.getLogger(__name__)
ogr.UseExceptions()


class Bbox2Gdal(object):

    formats = {
        'gjs': ["GeoJSON", "bag.geojson"],
        'gml': ["GML", "bag.gml"],
        'kml': ["KML", "bag.kml"],
        'shp': ["ESRI Shapefile", "bag.shp"],
    }

    def __init__(self, bag_meta: Meta, fmt="kml", title=None, out_file=None):
        self.bag_meta = bag_meta
        if not self.bag_meta.valid_bbox():
            raise BAGError("invalid bbox read in BAG metadata")

        self.title = title
        if self.title is None:
            self.title = "Metadata"
        logger.debug("title: %s" % self.title)

        # get the ogr driver
        self.drv = ogr.GetDriverByName(self.formats[fmt][0])
        if self.drv is None:
            raise BAGError("%s driver not available.\n" % self.formats[fmt][0])

        # set the output file
        self.out_file = out_file
        if self.out_file is None:
            self.out_file = os.path.abspath(self.formats[fmt][1])
            logger.debug("output: %s" % self.out_file)

        if os.path.exists(self.out_file):
            os.remove(self.out_file)

        # create the data source
        ds = self.drv.CreateDataSource(self.out_file)

        # create the spatial reference (WGS84)
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(4326)

        # create the layer
        self.lyr = ds.CreateLayer("BAG", self.srs, ogr.wkbLineString25D)
        self._define_layer_fields()

        # add feature
        self._add_feature()

        ds.Destroy()

    def _define_layer_fields(self):

        # Add the fields we're interested in
        self.lyr.CreateField(ogr.FieldDefn("Name", ogr.OFTString))
        if self.bag_meta.rows is not None:
            self.lyr.CreateField(ogr.FieldDefn("Rows", ogr.OFTInteger))
        if self.bag_meta.cols is not None:
            self.lyr.CreateField(ogr.FieldDefn("Cols", ogr.OFTInteger))
        if self.bag_meta.ne is not None:
            self.lyr.CreateField(ogr.FieldDefn("NE", ogr.OFTString))
        if self.bag_meta.sw is not None:
            self.lyr.CreateField(ogr.FieldDefn("SW", ogr.OFTString))
        if self.bag_meta.res_x is not None:
            self.lyr.CreateField(ogr.FieldDefn("ResX", ogr.OFTReal))
        if self.bag_meta.res_y is not None:
            self.lyr.CreateField(ogr.FieldDefn("ResY", ogr.OFTReal))
        if self.bag_meta.abstract is not None:
            self.lyr.CreateField(ogr.FieldDefn("Abstract", ogr.OFTString))
        if self.bag_meta.date is not None:
            self.lyr.CreateField(ogr.FieldDefn("Date", ogr.OFTString))
        if self.bag_meta.wkt_srs is not None:
            self.lyr.CreateField(ogr.FieldDefn("SRS", ogr.OFTString))
        self.lyr.CreateField(ogr.FieldDefn("Tools", ogr.OFTString))

    def _add_feature(self):
        # create the WKT for the feature using Python string formatting
        feature = ogr.Feature(self.lyr.GetLayerDefn())
        feature.SetField("Name", self.title)
        if self.bag_meta.rows is not None:
            feature.SetField("Rows", self.bag_meta.rows)
        if self.bag_meta.cols is not None:
            feature.SetField("Cols", self.bag_meta.cols)
        if self.bag_meta.ne is not None:
            feature.SetField("NE", ("%s" % self.bag_meta.ne))
        if self.bag_meta.sw is not None:
            feature.SetField("SW", ("%s" % self.bag_meta.sw))
        if self.bag_meta.res_x is not None:
            feature.SetField("ResX", ("%s" % self.bag_meta.res_x))
        if self.bag_meta.res_y is not None:
            feature.SetField("ResY", ("%s" % self.bag_meta.res_y))
        if self.bag_meta.abstract is not None:
            feature.SetField("Abstract", self.bag_meta.abstract)
        if self.bag_meta.date is not None:
            feature.SetField("Date", self.bag_meta.date)
        if self.bag_meta.wkt_srs is not None:
            feature.SetField("SRS", Helper.elide(self.bag_meta.wkt_srs, max_len=60))
        feature.SetField("Tools", ("r%s" % __version__))
        wkt = self.bag_meta.wkt_bbox()
        # log.debug("bbox: %s" % wkt)
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        self.lyr.CreateFeature(feature)
        feature.Destroy()
