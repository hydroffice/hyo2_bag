import os
import logging
from typing import Tuple

from osgeo import osr
import numpy as np
from lxml import etree, isoschematron

from hyo2.bag.base import is_bag, File
from hyo2.bag.helper import BAGError, Helper
from hyo2.bag.meta import Meta

logger = logging.getLogger(__name__)


class BAGFile(File):
    """ Represents a BAG file. """

    _bag_root = "BAG_root"
    _bag_version_tag = "Bag Version"
    _bag_version_number = b'1.6.3'
    _bag_elevation = "BAG_root/elevation"
    _bag_elevation_min_ev = "Minimum Elevation Value"
    _bag_elevation_max_ev = "Maximum Elevation Value"
    _bag_metadata = "BAG_root/metadata"
    _bag_tracking_list = "BAG_root/tracking_list"
    _bag_tracking_list_len = "Tracking List Length"
    _bag_tracking_list_type = np.dtype([('row', np.uint32), ('col', np.uint32),
                                        ('depth', np.float32), ('uncertainty', np.float32),
                                        ('track_code', np.byte), ('list_series', np.uint16)])
    _bag_uncertainty = "BAG_root/uncertainty"
    _bag_uncertainty_min_uv = "Minimum Uncertainty Value"
    _bag_uncertainty_max_uv = "Maximum Uncertainty Value"
    _bag_elevation_solution = "BAG_root/elevation_solution"

    _bag_varres_metadata = "BAG_root/varres_metadata"
    _bag_varres_refinements = "BAG_root/varres_refinements"
    _bag_varres_tracking_list = "BAG_root/varres_tracking_list"

    BAG_NAN = 1000000

    default_metadata_file = "BAG_metadata.xml"

    def __init__(self, name, mode='r', driver=None,
                 libver=None, userblock_size=None, swmr=False, **kwds):
        """
        Create a new file object.

        See the low level bag.File for a detailed explanation of the options.
        """
        if mode is not None:
            if 'w' not in mode:
                if not is_bag(name):
                    raise BAGError("The passed file %s is not a BAG file")

        super(BAGFile, self).__init__(name=name, mode=mode, driver=driver,
                                      libver=libver, userblock_size=userblock_size, swmr=swmr, **kwds)

        self.meta = None
        self.meta_errors = list()
        self._str = None

    @classmethod
    def is_bag(cls, bag_path: str, advanced: bool = False) -> bool:
        if not advanced:
            return os.path.splitext(bag_path)[-1].lower() == ".bag"

        raise RuntimeError("Not implemented")

    @classmethod
    def is_vr(cls, bag_path: str, advanced: bool = False) -> bool:
        if not advanced:
            return BAGFile(bag_path).has_varres_refinements()

        raise RuntimeError("Not implemented")

    @classmethod
    def create_template(cls, name):
        """ create a BAG file with empty template structure """
        logger.debug("create new BAG file: %s" % name)
        try:
            new_bag = File(name, 'w')
            new_bag.create_group(cls._bag_root)
            new_bag.attrs.create(cls._bag_version_tag, cls._bag_version_number, shape=(), dtype="S5")

            elevation = new_bag.create_dataset(cls._bag_elevation, shape=(), dtype=np.float32)
            elevation.attrs.create(cls._bag_elevation_min_ev, 0.0, shape=(), dtype=np.float32)
            elevation.attrs.create(cls._bag_elevation_max_ev, 0.0, shape=(), dtype=np.float32)

            new_bag.create_dataset(cls._bag_metadata, shape=(1,), dtype="S1")

            tracking_list = new_bag.create_dataset(cls._bag_tracking_list, shape=(), dtype=cls._bag_tracking_list_type)
            tracking_list.attrs.create(cls._bag_tracking_list_len, 0, shape=(), dtype=np.uint32)

            uncertainty = new_bag.create_dataset(cls._bag_uncertainty, shape=(), dtype=np.float32)
            uncertainty.attrs.create(cls._bag_uncertainty_min_uv, 0.0, shape=(), dtype=np.float32)
            uncertainty.attrs.create(cls._bag_uncertainty_max_uv, 0.0, shape=(), dtype=np.float32)

        except (BAGError, OSError) as e:
            raise BAGError("Unable to create the BAG file %s: %s" % (name, e))

        return new_bag

    def has_bag_root(self):
        return self._bag_root in self

    def has_bag_version(self):
        return self._bag_version_tag in self[self._bag_root].attrs

    def bag_version(self) -> str:
        return self[self._bag_root].attrs[self._bag_version_tag]

    def has_metadata(self):
        return BAGFile._bag_metadata in self

    def has_elevation(self):
        return BAGFile._bag_elevation in self

    def elevation(self, mask_nan=True, row_range=None):
        """
        Return the elevation as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        row_range
            If present, a slice of rows to read from
        """
        if row_range:
            if not isinstance(row_range, slice):
                raise BAGError("Invalid type of slice selector: %s" % type(row_range))
            if (row_range.start < 0) or (row_range.start >= self.elevation_shape()[0]) \
                    or (row_range.stop < 0) or (row_range.stop > self.elevation_shape()[0]) \
                    or (row_range.start > row_range.stop):
                raise BAGError("Invalid values for slice selector: %s" % row_range)

        if mask_nan:
            if row_range:
                el = self[BAGFile._bag_elevation][row_range]
            else:
                el = self[BAGFile._bag_elevation][:]
            mask = el == BAGFile.BAG_NAN
            el[mask] = np.nan
            return el

        if row_range:
            return self[BAGFile._bag_elevation][row_range]
        else:
            return self[BAGFile._bag_elevation][:]

    def elevation_shape(self):
        return self[BAGFile._bag_elevation].shape

    def elevation_min_max(self) -> Tuple[float, float]:
        rows, cols = self.elevation_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        mem_row = cols * 32 / 1024 / 1024
        # mem = mem_row * rows
        # logger.debug('estimated memory: %.1f MB' % mem)
        chunk_size = 8096
        chunk_rows = int(chunk_size / mem_row) + 1
        # logger.debug('nr of rows per chunk: %s' % chunk_rows)

        elv_min = np.nan
        elv_max = np.nan
        for start in range(0, rows, chunk_rows):
            stop = start + chunk_rows
            if stop > rows:
                stop = rows
            # logger.debug('slice: %s-%s' % (start, stop))
            _min = np.nanmin(self.elevation(row_range=slice(start, stop)))
            if np.isnan(elv_min):
                elv_min = _min
            else:
                if _min < elv_min:
                    elv_min = _min
            _max = np.nanmax(self.elevation(row_range=slice(start, stop)))
            if np.isnan(elv_max):
                elv_max = _max
            else:
                if _max > elv_max:
                    elv_max = _max

        return elv_min, elv_max

    def depth_min_max(self) -> Tuple[float, float]:
        elv_min, elv_max = self.elevation_min_max()
        return -elv_max, -elv_min

    def vr_refinements_shape(self):
        return self[BAGFile._bag_varres_refinements].shape

    def vr_elevation_min_max(self) -> Tuple[float, float]:
        # rows, cols = self.vr_refinements_shape()
        # logger.debug('refinements shape: %s, %s' % (rows, cols))

        vr_el = self[BAGFile._bag_varres_refinements][0]['depth']
        mask = vr_el == BAGFile.BAG_NAN
        vr_el[mask] = np.nan

        # logger.debug(vr_el)

        return np.nanmin(vr_el), np.nanmax(vr_el)

    def vr_depth_min_max(self) -> Tuple[float, float]:
        elv_min, elv_max = self.vr_elevation_min_max()
        return -elv_max, -elv_min

    def has_uncertainty(self):
        return BAGFile._bag_uncertainty in self

    def has_product_uncertainty(self):
        if self.has_uncertainty() and \
                (self.meta.unc_type == "productUncert" or self.meta.unc_type == "ProductUncert"):  # Leidos bug
            return True
        return False

    def uncertainty(self, mask_nan=True, row_range=None):
        """
        Return the uncertainty as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        row_range
            If present, a slice of rows to read from
        """
        if row_range:
            if not isinstance(row_range, slice):
                raise BAGError("Invalid type of slice selector: %s" % type(row_range))
            if (row_range.start < 0) or (row_range.start >= self.uncertainty_shape()[0]) \
                    or (row_range.stop < 0) or (row_range.stop > self.uncertainty_shape()[0]) \
                    or (row_range.start > row_range.stop):
                raise BAGError("Invalid values for slice selector: %s" % row_range)

        if mask_nan:
            if row_range:
                un = self[BAGFile._bag_uncertainty][row_range]
            else:
                un = self[BAGFile._bag_uncertainty][:]
            mask = un == BAGFile.BAG_NAN
            un[mask] = np.nan
            return un

        if row_range:
            return self[BAGFile._bag_uncertainty][row_range]
        else:
            return self[BAGFile._bag_uncertainty][:]

    def uncertainty_shape(self):
        return self[BAGFile._bag_uncertainty].shape

    def uncertainty_min_max(self) -> Tuple[float, float]:
        rows, cols = self.uncertainty_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        mem_row = cols * 32 / 1024 / 1024
        # mem = mem_row * rows
        # logger.debug('estimated memory: %.1f MB' % mem)
        chunk_size = 8096
        chunk_rows = int(chunk_size / mem_row) + 1
        # logger.debug('nr of rows per chunk: %s' % chunk_rows)

        unc_min = np.nan
        unc_max = np.nan
        for start in range(0, rows, chunk_rows):
            stop = start + chunk_rows
            if stop > rows:
                stop = rows
            # logger.debug('slice: %s-%s' % (start, stop))
            _min = np.nanmin(self.uncertainty(row_range=slice(start, stop)))
            if np.isnan(unc_min):
                unc_min = _min
            else:
                if _min < unc_min:
                    unc_min = _min
            _max = np.nanmax(self.uncertainty(row_range=slice(start, stop)))
            if np.isnan(unc_max):
                unc_max = _max
            else:
                if _max > unc_max:
                    unc_max = _max

        return unc_min, unc_max

    def uncertainty_greater_than(self, th: float) -> list[list[int | float]]:
        rows, cols = self.uncertainty_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        self.populate_metadata()

        x_min = self.meta.sw[0]
        y_min = self.meta.sw[1]
        x_res = self.meta.res_x
        y_res = self.meta.res_y
        # logger.debug("info: %f %f %f %f" % (x_min, y_min, x_res, y_res))

        in_srs = osr.SpatialReference()
        in_srs.ImportFromWkt(self.meta.wkt_srs)
        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(4326)
        out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        ctr = osr.CoordinateTransformation(in_srs, out_srs)

        mem_row = cols * 32 / 1024 / 1024
        # mem = mem_row * rows
        # logger.debug('estimated memory: %.1f MB' % mem)
        chunk_size = 8096
        chunk_rows = int(chunk_size / mem_row) + 1
        # logger.debug('nr of rows per chunk: %s' % chunk_rows)

        xyz = list()
        for start in range(0, rows, chunk_rows):
            stop = start + chunk_rows
            if stop > rows:
                stop = rows

            unc = self.uncertainty(row_range=slice(start, stop))
            ijs = np.argwhere(unc > th)
            for ij in ijs:
                i = ij[0]
                j = ij[1]
                e = x_min + j * x_res
                n = y_min + (start + i) * y_res
                lat, lon, _ = ctr.TransformPoint(e, n)
                u = float(unc[i, j])
                xyz.append([float(lat), float(lon), u])
                # logger.info("%d,%d: %.7f %.7f %.3f" % ((start + i), j, xyz[-1][0], xyz[-1][1], xyz[-1][2]))

        return xyz

    def uncertainty_has_depth(self) -> list[list[int | float]]:
        rows, cols = self.uncertainty_shape()
        # logger.debug('shape: %s, %s (%d)' % (rows, cols, rows * cols))

        self.populate_metadata()

        x_min = self.meta.sw[0]
        y_min = self.meta.sw[1]
        x_res = self.meta.res_x
        y_res = self.meta.res_y
        # logger.debug("info: %f %f %f %f" % (x_min, y_min, x_res, y_res))

        in_srs = osr.SpatialReference()
        in_srs.ImportFromWkt(self.meta.wkt_srs)
        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(4326)
        out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        ctr = osr.CoordinateTransformation(in_srs, out_srs)

        mem_row = cols * 32 / 1024 / 1024
        # mem = mem_row * rows
        # logger.debug('estimated memory: %.1f MB' % mem)
        chunk_size = 8096
        chunk_rows = int(chunk_size / mem_row) + 1
        # logger.debug('nr of rows per chunk: %s' % chunk_rows)

        xyz = list()
        for start in range(0, rows, chunk_rows):
            stop = start + chunk_rows
            if stop > rows:
                stop = rows

            unc = self.uncertainty(row_range=slice(start, stop))
            # logger.info("unc: %d, %d" % (np.isnan(unc).sum(), np.isfinite(unc).sum()))
            dep = self.elevation(row_range=slice(start, stop))
            # logger.info("dep: %d, %d" % (np.isnan(dep).sum(), np.isfinite(dep).sum()))
            unc[np.isfinite(dep)] = np.nan
            # logger.info(unc)
            ijs = np.argwhere(np.isfinite(unc))
            # logger.info(ijs)
            for ij in ijs:
                i = ij[0]
                j = ij[1]
                e = x_min + j * x_res
                n = y_min + (start + i) * y_res
                lat, lon, _ = ctr.TransformPoint(e, n)
                u = float(unc[i, j])
                xyz.append([float(lat), float(lon), u])
                # logger.info("%d,%d: %.7f %.7f %.3f" % ((start + i), j, xyz[-1][0], xyz[-1][1], xyz[-1][2]))

        return xyz

    def depth_has_uncertainty(self) -> list[list[int | float]]:
        rows, cols = self.uncertainty_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        self.populate_metadata()

        x_min = self.meta.sw[0]
        y_min = self.meta.sw[1]
        x_res = self.meta.res_x
        y_res = self.meta.res_y
        # logger.debug("info: %f %f %f %f" % (x_min, y_min, x_res, y_res))

        in_srs = osr.SpatialReference()
        in_srs.ImportFromWkt(self.meta.wkt_srs)
        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(4326)
        out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        ctr = osr.CoordinateTransformation(in_srs, out_srs)

        mem_row = cols * 32 / 1024 / 1024
        # mem = mem_row * rows
        # logger.debug('estimated memory: %.1f MB' % mem)
        chunk_size = 8096
        chunk_rows = int(chunk_size / mem_row) + 1
        # logger.debug('nr of rows per chunk: %s' % chunk_rows)

        xyz = list()
        for start in range(0, rows, chunk_rows):
            stop = start + chunk_rows
            if stop > rows:
                stop = rows

            unc = self.uncertainty(row_range=slice(start, stop))
            # logger.info(unc)
            dep = self.elevation(row_range=slice(start, stop))
            # logger.info(dep)
            dep[np.isfinite(unc)] = np.nan
            # logger.info(dep)
            ijs = np.argwhere(np.isfinite(dep))
            # logger.info(ijs)
            for ij in ijs:
                i = ij[0]
                j = ij[1]
                e = x_min + j * x_res
                n = y_min + (start + i) * y_res
                lat, lon, _ = ctr.TransformPoint(e, n)
                z = -float(dep[i, j])
                xyz.append([float(lat), float(lon), z])
                # logger.info("%d,%d: %.7f %.7f %.3f" % ((start + i), j, xyz[-1][0], xyz[-1][1], xyz[-1][2]))

        return xyz

    def vr_uncertainty_min_max(self) -> Tuple[float, float]:
        # rows, cols = self.vr_refinements_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        vr_unc = self[BAGFile._bag_varres_refinements][0]['depth_uncrt']
        mask = vr_unc == BAGFile.BAG_NAN
        vr_unc[mask] = np.nan

        # logger.debug(vr_el)

        return np.nanmin(vr_unc), np.nanmax(vr_unc)

    def vr_uncertainty_greater_than(self, th: float) -> list[list[int | float]]:
        # rows, cols = self.vr_refinements_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        self.populate_metadata()

        x_min = self.meta.sw[0]
        y_min = self.meta.sw[1]
        x_res = self.meta.res_x
        y_res = self.meta.res_y
        # logger.debug("info: %f %f %f %f" % (x_min, y_min, x_res, y_res))

        in_srs = osr.SpatialReference()
        in_srs.ImportFromWkt(self.meta.wkt_srs)
        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(4326)
        out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        ctr = osr.CoordinateTransformation(in_srs, out_srs)

        vr_unc = self[BAGFile._bag_varres_refinements][0]['depth_uncrt']
        mask = vr_unc == BAGFile.BAG_NAN
        vr_unc[mask] = np.nan

        xyz_dict = dict()
        for idx, unc in enumerate(vr_unc):
            if unc > th:
                xyz_dict[idx] = unc

        # logger.info("Located %d outliers" % len(xyz_dict))

        xyz = list()
        vr_ixs = self[BAGFile._bag_varres_metadata][:]
        rows, cols = vr_ixs.shape
        i = 0
        for sg_r in range(rows):
            for sg_c in range(cols):
                if vr_ixs[sg_r, sg_c][1] == 0:
                    continue
                ir = vr_ixs[sg_r, sg_c][1] * vr_ixs[sg_r, sg_c][2]
                for ir_idx in range(ir):
                    j = i + ir_idx
                    if j not in xyz_dict:
                        continue
                    unc = float(xyz_dict[j])
                    # logger.debug("Located outliers: %d %f in %d,%d: %s" % (j, unc, sg_r, sg_c, vr_ixs[sg_r, sg_c]))
                    # vr_ixs[r, c]
                    rfn_r = ir_idx // vr_ixs[sg_r, sg_c][1]
                    rfn_c = ir_idx % vr_ixs[sg_r, sg_c][1]
                    # logger.debug("%d > %d,%d" % (ir_idx, rfn_r, rfn_c))
                    e = x_min + (sg_c - 0.5) * x_res + vr_ixs[sg_r, sg_c][5] + rfn_c * vr_ixs[sg_r, sg_c][3]
                    n = y_min + (sg_r - 0.5) * y_res + vr_ixs[sg_r, sg_c][6] + rfn_r * vr_ixs[sg_r, sg_c][4]
                    lat, lon, _ = ctr.TransformPoint(e, n)
                    xyz.append([float(lat), float(lon), unc])
                i += ir

        return xyz

    def vr_depth_has_uncertainty(self) -> list[list[int | float]]:
        # rows, cols = self.vr_refinements_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        self.populate_metadata()

        x_min = self.meta.sw[0]
        y_min = self.meta.sw[1]
        x_res = self.meta.res_x
        y_res = self.meta.res_y
        # logger.debug("info: %f %f %f %f" % (x_min, y_min, x_res, y_res))

        in_srs = osr.SpatialReference()
        in_srs.ImportFromWkt(self.meta.wkt_srs)
        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(4326)
        out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        ctr = osr.CoordinateTransformation(in_srs, out_srs)

        vr_unc = self[BAGFile._bag_varres_refinements][0]['depth_uncrt']
        mask = vr_unc == BAGFile.BAG_NAN
        vr_unc[mask] = np.nan
        vr_dep = self[BAGFile._bag_varres_refinements][0]['depth']
        mask = vr_dep == BAGFile.BAG_NAN
        vr_dep[mask] = np.nan

        xyz_dict = dict()
        for idx, unc in enumerate(vr_unc):
            dep = vr_dep[idx]
            if np.isfinite(dep) and np.isnan(unc):
                xyz_dict[idx] = dep

        # logger.info("Located %d outliers" % len(xyz_dict))

        xyz = list()
        vr_ixs = self[BAGFile._bag_varres_metadata][:]
        rows, cols = vr_ixs.shape
        i = 0
        for sg_r in range(rows):
            for sg_c in range(cols):
                if vr_ixs[sg_r, sg_c][1] == 0:
                    continue
                ir = vr_ixs[sg_r, sg_c][1] * vr_ixs[sg_r, sg_c][2]
                for ir_idx in range(ir):
                    j = i + ir_idx
                    if j not in xyz_dict:
                        continue
                    dep = float(xyz_dict[j])
                    # logger.debug("Located outliers: %d %f in %d,%d: %s" % (j, unc, sg_r, sg_c, vr_ixs[sg_r, sg_c]))
                    # vr_ixs[r, c]
                    rfn_r = ir_idx // vr_ixs[sg_r, sg_c][1]
                    rfn_c = ir_idx % vr_ixs[sg_r, sg_c][1]
                    # logger.debug("%d > %d,%d" % (ir_idx, rfn_r, rfn_c))
                    e = x_min + (sg_c - 0.5) * x_res + vr_ixs[sg_r, sg_c][5] + rfn_c * vr_ixs[sg_r, sg_c][3]
                    n = y_min + (sg_r - 0.5) * y_res + vr_ixs[sg_r, sg_c][6] + rfn_r * vr_ixs[sg_r, sg_c][4]
                    lat, lon, _ = ctr.TransformPoint(e, n)
                    xyz.append([float(lat), float(lon), dep])
                i += ir

        return xyz

    def vr_uncertainty_has_depth(self) -> list[list[int | float]]:
        # rows, cols = self.vr_refinements_shape()
        # logger.debug('shape: %s, %s' % (rows, cols))

        self.populate_metadata()

        x_min = self.meta.sw[0]
        y_min = self.meta.sw[1]
        x_res = self.meta.res_x
        y_res = self.meta.res_y
        # logger.debug("info: %f %f %f %f" % (x_min, y_min, x_res, y_res))

        in_srs = osr.SpatialReference()
        in_srs.ImportFromWkt(self.meta.wkt_srs)
        out_srs = osr.SpatialReference()
        out_srs.ImportFromEPSG(4326)
        out_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        ctr = osr.CoordinateTransformation(in_srs, out_srs)

        vr_unc = self[BAGFile._bag_varres_refinements][0]['depth_uncrt']
        mask = vr_unc == BAGFile.BAG_NAN
        vr_unc[mask] = np.nan
        vr_dep = self[BAGFile._bag_varres_refinements][0]['depth']
        mask = vr_dep == BAGFile.BAG_NAN
        vr_dep[mask] = np.nan

        xyz_dict = dict()
        for idx, unc in enumerate(vr_unc):
            dep = vr_dep[idx]
            if np.isfinite(unc) and np.isnan(dep):
                xyz_dict[idx] = unc

        # logger.info("Located %d outliers" % len(xyz_dict))

        xyz = list()
        vr_ixs = self[BAGFile._bag_varres_metadata][:]
        rows, cols = vr_ixs.shape
        i = 0
        for sg_r in range(rows):
            for sg_c in range(cols):
                if vr_ixs[sg_r, sg_c][1] == 0:
                    continue
                ir = vr_ixs[sg_r, sg_c][1] * vr_ixs[sg_r, sg_c][2]
                for ir_idx in range(ir):
                    j = i + ir_idx
                    if j not in xyz_dict:
                        continue
                    unc = float(xyz_dict[j])
                    # logger.debug("Located outliers: %d %f in %d,%d: %s" % (j, unc, sg_r, sg_c, vr_ixs[sg_r, sg_c]))
                    # vr_ixs[r, c]
                    rfn_r = ir_idx // vr_ixs[sg_r, sg_c][1]
                    rfn_c = ir_idx % vr_ixs[sg_r, sg_c][1]
                    # logger.debug("%d > %d,%d" % (ir_idx, rfn_r, rfn_c))
                    e = x_min + (sg_c - 0.5) * x_res + vr_ixs[sg_r, sg_c][5] + rfn_c * vr_ixs[sg_r, sg_c][3]
                    n = y_min + (sg_r - 0.5) * y_res + vr_ixs[sg_r, sg_c][6] + rfn_r * vr_ixs[sg_r, sg_c][4]
                    lat, lon, _ = ctr.TransformPoint(e, n)
                    xyz.append([float(lat), float(lon), unc])
                i += ir

        return xyz

    def has_density(self):
        # noinspection PyBroadException
        try:
            self[BAGFile._bag_elevation_solution]['num_soundings']
        except Exception:
            return False
        return True

    def density(self, mask_nan=True, row_range=None):
        """
        Return the density as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        row_range
            If present, a slice of rows to read from
        """
        if row_range:
            if not isinstance(row_range, slice):
                raise BAGError("Invalid type of slice selector: %s" % type(row_range))
            if (row_range.start < 0) or (row_range.start >= self.density_shape()[0]) \
                    or (row_range.stop < 0) or (row_range.stop > self.density_shape()[0]) \
                    or (row_range.start > row_range.stop):
                raise BAGError("Invalid values for slice selector: %s" % row_range)

        if mask_nan:
            if row_range:
                de = self[BAGFile._bag_elevation_solution]['num_soundings'][row_range]
            else:
                de = self[BAGFile._bag_elevation_solution]['num_soundings'][:]
            de = de.astype(float)
            mask = de == BAGFile.BAG_NAN
            de[mask] = np.nan
            return de

        if row_range:
            de = self[BAGFile._bag_elevation_solution]['num_soundings'][row_range]
        else:
            de = self[BAGFile._bag_elevation_solution]['num_soundings'][:]
        de = de.astype(float)
        return de

    def density_shape(self):
        return self[BAGFile._bag_elevation_solution].shape

    def has_tracking_list(self):
        return BAGFile._bag_tracking_list in self

    def tracking_list(self):
        """ Return the tracking list as numpy array """
        return self[BAGFile._bag_tracking_list][:]

    def tracking_list_fields(self):
        """ Return the tracking list field names """
        return self[BAGFile._bag_tracking_list].dtype.names

    def tracking_list_types(self):
        """ Return the tracking list field names """
        return self[BAGFile._bag_tracking_list].dtype

    def has_valid_row_in_tracking_list(self):
        rows, _ = self.elevation_shape()
        # logger.info('rows: %s, cols: %s' % (rows, _))

        tl = self.tracking_list()
        for idx, row in enumerate(tl['row']):
            if row >= rows:
                logger.warning("%d 'row' entry is invalid: %s" % (idx, row))
                return False

        return True

    def has_valid_col_in_tracking_list(self):
        rows, cols = self.elevation_shape()
        # logger.info('rows: %s, cols: %s' % (rows, cols))

        tl = self.tracking_list()
        for idx, col in enumerate(tl['col']):
            if col >= cols:
                logger.warning("%d 'col' entry is invalid: %s" % (idx, col))
                return False

        return True

    def metadata(self, as_string=True, as_pretty_xml=True):
        """ Return the metadata

        as_string
            If True, convert the metadata from a dataset of characters to a string
        as_pretty_xml
            If True, return the xml in a pretty format as bytes
        """
        xml_bytes = self[BAGFile._bag_metadata][:].tostring().strip(b'\x00')

        if as_pretty_xml:
            xml_tree = etree.fromstring(xml_bytes)
            pretty_bytes = etree.tostring(xml_tree, pretty_print=True)
            if as_string:
                return pretty_bytes.decode()
            return pretty_bytes
        else:
            if as_string:
                return xml_bytes.decode()
            return xml_bytes

    def extract_metadata(self, name=None):
        """ Save metadata on disk

        name
            The file path where the metadata will be saved. If None, use a default name.
        """

        meta_xml = self.metadata(as_pretty_xml=True)
        if meta_xml is None:
            logger.info("unable to access the metadata")
            return

        if name is None:
            name = os.path.join(self.default_metadata_file)

        with open(os.path.abspath(name), 'w') as fid:
            fid.write(meta_xml.decode())

    def substitute_metadata(self, path):
        """ Substitute internal metadata

        name
            The file path where the new metadata are.
        """

        path = os.path.abspath(path)
        if not os.path.exists(path):
            logger.info("the passed file does not exist")
            return

        with open(path, 'r') as fid:
            xml_string = str.encode(fid.read())

        is_valid = self.validate_metadata(xml_string)
        if not is_valid:
            logger.info("the passed metadata file is not valid")
            return

        del self[BAGFile._bag_metadata]
        xml_sz = len(xml_string)
        ds = self.create_dataset(self._bag_metadata, (xml_sz,), dtype="S1")
        for i, bt in enumerate(xml_string):
            ds[i] = bytes([bt])

    def validate_metadata(self, xml_string: None | bytes = None) -> bool:
        """ Validate metadata based on XML Schemas and schematron. """
        # clean metadata error list
        self.meta_errors = list()
        # assuming a valid BAG
        is_valid = True

        if xml_string is None:
            xml_string = self.metadata(as_pretty_xml=True)

        try:
            xml_tree = etree.fromstring(xml_string)
        except etree.Error as e:
            logger.warning("unable to parse XML metadata: %s" % e)
            self.meta_errors.append(e)
            return False

        try:
            schema_path = os.path.join(Helper.iso19139_folder(), 'bag', 'bag.xsd')
            schema_doc = etree.parse(schema_path)
            schema = etree.XMLSchema(schema_doc)
        except etree.Error as e:
            logger.warning("unable to parse XML schema: %s" % e)
            self.meta_errors.append(e)
            return False

        try:
            schema.assertValid(xml_tree)
        except etree.DocumentInvalid as e:
            logger.warning("invalid metadata based on XML schema: %s" % e)
            self.meta_errors.append(e)
            for i in schema.error_log:
                self.meta_errors.append(i)
            is_valid = False

        if is_valid:
            logger.debug("xsd validated")

        try:
            schematron_path = os.path.join(Helper.iso19757_3_folder(), 'bag_metadata_profile.sch')
            schematron_doc = etree.parse(schematron_path)
        except etree.DocumentInvalid as e:
            logger.warning("unable to parse BAG schematron: %s" % e)
            self.meta_errors.append(e)
            return False

        try:
            schematron = isoschematron.Schematron(schematron_doc, store_report=True)
        except etree.DocumentInvalid as e:
            logger.warning("unable to load BAG schematron: %s" % e)
            self.meta_errors.append(e)
            return False

        if schematron.validate(xml_tree):
            logger.debug("schematron validated")
        else:
            logger.warning("invalid metadata based on Schematron")
            is_valid = False
            ns = {
                'svrl': 'http://purl.oclc.org/dsdl/svrl',
            }
            for i in schematron.error_log:
                err_tree = etree.fromstring(i.message)
                # print(etree.tostring(err_tree, pretty_print=True))
                err_msg = err_tree.xpath('/svrl:failed-assert/svrl:text', namespaces=ns)[0].text.strip()
                logger.warning(err_msg)
                self.meta_errors.append(err_msg)

        return is_valid

    def validation_info(self):
        """ Return a message string with the result of the validation """
        msg = str()

        msg += "XML input source: %s\nValidation output: " % self._bag_metadata
        if self.validate_metadata():
            msg += "VALID"
        else:
            msg += "INVALID\nReasons:\n"
            for err_msg in self.meta_errors:
                msg += " - %s\n" % err_msg
        return msg

    def populate_metadata(self):
        """ Populate metadata class """

        if self.meta is not None:
            # log.debug("metadata already populated")
            return self.meta

        self.meta = Meta(meta_xml=self.metadata(as_pretty_xml=True))
        return self.meta

    def modify_wkt_prj(self, wkt_hor, wkt_ver=None):
        """ Modify the wkt prj in the metadata content

        text
            The new wkt prj text to use
        """
        ns = {
            'bag': 'http://www.opennavsurf.org/schema/bag',
            'gco': 'http://www.isotc211.org/2005/gco',
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gmi': 'http://www.isotc211.org/2005/gmi',
            'gml': 'http://www.opengis.net/gml/3.2',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }

        # print(self[BAGFile._bag_metadata][:])
        xml_tree = etree.fromstring(self[BAGFile._bag_metadata][:].tostring())

        try:
            ret = xml_tree.xpath('//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                 'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                 namespaces=ns)
            ret[0].text = wkt_hor
            if wkt_ver is not None:
                ret[1].text = wkt_ver

        except etree.Error as e:
            logger.warning("unable to read the WKT projection string: %s" % e)
            return

        new_xml = etree.tostring(xml_tree, pretty_print=True)
        del self[BAGFile._bag_metadata]
        ds = self.create_dataset(BAGFile._bag_metadata, shape=(len(new_xml),), dtype="S1")
        for i, x in enumerate(new_xml):
            ds[i] = bytes([x])

    def modify_bbox(self, west, east, south, north):
        """ attempts to modify the bounding box values """
        ns = {
            'bag': 'http://www.opennavsurf.org/schema/bag',
            'gco': 'http://www.isotc211.org/2005/gco',
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gmi': 'http://www.isotc211.org/2005/gmi',
            'gml': 'http://www.opengis.net/gml/3.2',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }

        xml_tree = etree.fromstring(self[BAGFile._bag_metadata][:].tostring())

        try:
            ret_x_min = xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal',
                                       namespaces=ns)
            ret_x_max = xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal',
                                       namespaces=ns)
        except etree.Error as e:
            logger.warning("unable to read the bbox's longitude values: %s" % e)
            return

        try:
            ret_x_min[0].text = "%s" % west
            ret_x_max[0].text = "%s" % east
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the bbox's longitude values: %s" % e)
            return

        try:
            ret_y_min = xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal',
                                       namespaces=ns)
            ret_y_max = xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal',
                                       namespaces=ns)
        except etree.Error as e:
            logger.warning("unable to read the bbox's latitude values: %s" % e)
            return

        try:
            ret_y_min[0].text = "%s" % south
            ret_y_max[0].text = "%s" % north
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the bbox's latitude values: %s" % e)
            return

        new_xml = etree.tostring(xml_tree, pretty_print=True)
        del self[BAGFile._bag_metadata]
        ds = self.create_dataset(BAGFile._bag_metadata, shape=(len(new_xml),), dtype="S1")
        for i, x in enumerate(new_xml):
            ds[i] = bytes([x])

    def has_varres_metadata(self):
        return BAGFile._bag_varres_metadata in self

    def has_varres_refinements(self):
        return BAGFile._bag_varres_refinements in self

    def has_varres_tracking_list(self):
        return BAGFile._bag_varres_tracking_list in self

    def _str_group_info(self, grp):
        if grp == self._bag_root:
            self._str += "  <root>\n"
        elif grp == self._bag_elevation:
            self._str += "  <elevation shape=%s>\n" % str(self.elevation().shape)
        elif grp == self._bag_uncertainty:
            self._str += "  <uncertainty shape=%s>\n" % str(self.uncertainty().shape)
        elif grp == self._bag_tracking_list:
            self._str += "  <tracking list shape=%s>\n" % str(self.tracking_list().shape)
        elif grp == self._bag_metadata:
            if self.meta is not None:
                self._str += "  %s\n" % str(self.meta)
            else:
                self._str += "  <%s>\n" % grp
        else:
            self._str += "  <%s>\n" % grp

        if grp != self._bag_metadata:
            for atr in self[grp].attrs:
                atr_val = self[grp].attrs[atr]
                self._str += "    <%s: %s (%s, %s)>\n" % (atr, atr_val, atr_val.shape, atr_val.dtype)

    def __str__(self):
        self._str = super(BAGFile, self).__str__()
        self.visit(self._str_group_info)
        return self._str
