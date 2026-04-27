import logging
from datetime import datetime

import dateutil.parser
from lxml import etree
from osgeo import osr

# noinspection PyUnresolvedReferences
from hyo2.abc2.lib.gdal_aux import GdalAux
# noinspection PyUnresolvedReferences
from hyo2.bag.helper import Helper

logger = logging.getLogger(__name__)


class Meta:
    """ Helper class to manage BAG XML metadata. """

    # noinspection HttpUrlsUsage
    ns = {
        'bag': 'http://www.opennavsurf.org/schema/bag',
        'gco': 'http://www.isotc211.org/2005/gco',
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gmi': 'http://www.isotc211.org/2005/gmi',
        'gml': 'http://www.opengis.net/gml/3.2',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    }

    # noinspection HttpUrlsUsage
    ns2 = {
        'gml': 'http://www.opengis.net/gml',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'smXML': 'http://metadata.dgiwg.org/smXML',
    }

    def __init__(self, meta_xml: bytes | str) -> None:
        GdalAux.push_gdal_error_handler()

        # noinspection PyUnresolvedReferences
        self.xml_tree = etree.fromstring(meta_xml)

        # rows and cols
        self._rows: int | None = None
        self._cols: int | None = None
        self._read_rows_and_cols()

        # resolution along x and y axes
        self._res_x: float | None = None
        self._res_y: float | None = None
        self._read_res_x_and_y()

        # corner SW and NE
        self._sw: list[float] | None = None
        self._ne: list[float] | None = None
        self._read_corners_sw_and_ne()

        # wkt projection
        self._wkt_srs: str | None = None
        self._xml_srs: str | None = None
        self._wkt_srs_epsg_code: int | None = None
        self._read_wkt_prj()

        # wkt vertical datum
        self._wkt_vertical_datum: str | None = None
        self._xml_vertical_datum: str | None = None
        self._wkt_vertical_datum_epsg_code: int | None = None
        self._read_wkt_vertical_datum()

        # bbox
        self._lon_min: float | None = None
        self._lon_max: float | None = None
        self._lat_min: float | None = None
        self._lat_max: float | None = None
        self._read_bbox()

        # abstract
        self._abstract: str | None = None
        self._read_abstract()

        # date
        self._date: datetime | str | None = None
        self._read_date()

        # survey dates
        self._survey_start_date: datetime | str | None = None
        self._read_survey_start_date()
        self._survey_end_date: datetime | str | None = None
        self._read_survey_end_date()

        # uncertainty type
        self._unc_type: str | None = None
        self._read_uncertainty_type()

        # security constraints
        self._sec_constr: str | None = None
        self._read_security_constraints()

    @property
    def rows(self) -> int:
        if self._rows is None:
            raise RuntimeError("Unpopulated _rows")
        return self._rows

    @property
    def cols(self) -> int:
        if self._cols is None:
            raise RuntimeError("Unpopulated _cols")
        return self._cols

    @property
    def res_x(self) -> float:
        if self._res_x is None:
            raise RuntimeError("Unpopulated _res_x")
        return self._res_x

    @property
    def res_y(self) -> float:
        if self._res_y is None:
            raise RuntimeError("Unpopulated _res_y")
        return self._res_y

    @property
    def sw(self) -> list[float]:
        if self._sw is None:
            raise RuntimeError("Unpopulated _sw")
        return self._sw

    @property
    def ne(self) -> list[float]:
        if self._ne is None:
            raise RuntimeError("Unpopulated _ne")
        return self._ne

    @property
    def wkt_srs(self) -> str:
        if self._wkt_srs is None:
            raise RuntimeError("Unpopulated _wrk_srs")
        return self._wkt_srs

    @property
    def xml_srs(self) -> str:
        if self._xml_srs is None:
            raise RuntimeError("Unpopulated _xml_srs")
        return self._xml_srs

    def has_wkt_srs_epsg_code(self) -> bool:
        return self._wkt_srs_epsg_code is not None

    @property
    def wkt_srs_epsg_code(self) -> int:
        if self._wkt_srs_epsg_code is None:
            raise RuntimeError("Unpopulated _xml_srs_epsg_code")
        return self._wkt_srs_epsg_code

    @property
    def wkt_vertical_datum(self) -> str:
        if self._wkt_vertical_datum is None:
            raise RuntimeError("Unpopulated _wkt_vertical_datum")
        return self._wkt_vertical_datum

    @property
    def xml_vertical_datum(self) -> str:
        if self._xml_vertical_datum is None:
            raise RuntimeError("Unpopulated _xml_vertical_datum")
        return self._xml_vertical_datum

    def has_wkt_vertical_datum_epsg_code(self) -> bool:
        return self._wkt_vertical_datum_epsg_code is not None

    @property
    def wkt_vertical_datum_epsg_code(self) -> int:
        if self._wkt_vertical_datum_epsg_code is None:
            raise RuntimeError("Unpopulated _wkt_vertical_datum_epsg_code")
        return self._wkt_vertical_datum_epsg_code

    @property
    def lon_min(self) -> float:
        if self._lon_min is None:
            raise RuntimeError("Unpopulated _lon_min")
        return self._lon_min

    @property
    def lon_max(self) -> float:
        if self._lon_max is None:
            raise RuntimeError("Unpopulated _lon_max")
        return self._lon_max

    @property
    def lat_min(self) -> float:
        if self._lat_min is None:
            raise RuntimeError("Unpopulated _lat_min")
        return self._lat_min

    @property
    def lat_max(self) -> float:
        if self._lat_max is None:
            raise RuntimeError("Unpopulated _lat_max")
        return self._lat_max

    @property
    def abstract(self) -> str:
        if self._abstract is None:
            raise RuntimeError("Unpopulated _abstract")
        return self._abstract

    @property
    def date(self) -> datetime | str:
        if self._date is None:
            raise RuntimeError("Unpopulated _date")
        return self._date

    @property
    def survey_start_date(self) -> datetime | str:
        if self._survey_start_date is None:
            raise RuntimeError("Unpopulated _survey_start_date")
        return self._survey_start_date

    @property
    def survey_end_date(self) -> datetime | str:
        if self._survey_end_date is None:
            raise RuntimeError("Unpopulated _survey_end_date")
        return self._survey_end_date

    @property
    def unc_type(self) -> str:
        if self._unc_type is None:
            raise RuntimeError("Unpopulated _unc_type")
        return self._unc_type

    @property
    def sec_constr(self) -> str:
        if self._sec_constr is None:
            raise RuntimeError("Unpopulated _sec_constr")
        return self._sec_constr

    def __str__(self) -> str:
        output = "<metadata>"

        if (self._rows is not None) and (self._cols is not None):
            output += "\n    <shape rows=%d, cols=%d>" % (self.rows, self.cols)

        if (self._res_x is not None) and (self._res_y is not None):
            output += "\n    <resolution x=%f, y=%f>" % (self.res_x, self.res_y)

        if (self._sw is not None) and (self._ne is not None):
            output += "\n    <corners SW=%s, NE=%s>" % (self.sw, self.ne)

        if self._wkt_srs is not None:
            output += "\n    <projection=%s>" % Helper.elide(self.wkt_srs, max_len=60)

        if self._date is not None:
            output += "\n    <date=%s>" % self.date

        if self._abstract is not None:
            output += "\n    <abstract=%s>" % self.abstract

        output += "\n    <bbox>"
        if (self._lon_min is not None) and (self._lon_max is not None):
            output += "\n        <x min=%s, max=%s>" % (self.lon_min, self.lon_max)
        if (self._lat_min is not None) and (self._lat_max is not None):
            output += "\n        <y min=%s, max=%s>" % (self.lat_min, self.lat_max)

        if self._unc_type is not None:
            output += "\n    <uncertainty type=%s>" % self.unc_type

        if self._sec_constr is not None:
            output += "\n    <security constraints=%s>" % self.sec_constr

        return output

    def valid_bbox(self) -> bool:
        return (self.lon_min is not None) and (self.lon_max is not None) and \
            (self.lat_min is not None) and (self.lat_max is not None)

    def geo_extent(self) -> tuple[float, float, float, float]:
        """ Return the geographic extent as a tuple: (x_min, x_max, y_min, y_max) """
        return self.lon_min, self.lon_max, self.lat_min, self.lat_max

    def wkt_bbox(self) -> str:
        return "LINESTRING Z(%.6f %.6f 0, %.6f %.6f 0, %.6f %.6f 0, %.6f %.6f 0, %.6f %.6f 0)" \
            % (self.lon_min, self.lat_min, self.lon_min, self.lat_max, self.lon_max, self.lat_max, self.lon_max,
               self.lat_min, self.lon_min, self.lat_min)

    def _read_rows_and_cols(self) -> None:
        """ attempts to read rows and cols info """

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:dimensionSize/gco:Integer',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read rows and cols: %s" % e)
            return

        if len(ret) == 0:

            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/spatialRepresentationInfo/smXML:MD_Georectified/'
                                          'axisDimensionProperties/smXML:MD_Dimension/dimensionSize',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read rows and cols: %s" % e)
                return

        try:
            self._rows = int(ret[0].text)
            self._cols = int(ret[1].text)

        except (ValueError, IndexError) as e:
            logger.warning("unable to read rows and cols: %s" % e)
            return

    def _read_res_x_and_y(self) -> None:
        """ attempts to read resolution along x- and y- axes """

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:resolution/gco:Measure',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read res x and y: %s" % e)
            return

        if len(ret) == 0:

            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/spatialRepresentationInfo/smXML:MD_Georectified/'
                                          'axisDimensionProperties/smXML:MD_Dimension/resolution/'
                                          'smXML:Measure/smXML:value',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read res x and y: %s" % e)
                return

        try:
            self._res_x = float(ret[0].text)
            self._res_y = float(ret[1].text)

        except (ValueError, IndexError) as e:
            logger.warning("unable to read res x and y: %s" % e)
            return

    def _read_corners_sw_and_ne(self) -> None:
        """ attempts to read corners SW and NE """

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:cornerPoints/gml:Point/gml:coordinates',
                                      namespaces=self.ns)[0].text.split()
        except (etree.Error, IndexError):
            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/spatialRepresentationInfo/smXML:MD_Georectified/'
                                          'cornerPoints/gml:Point/gml:coordinates',
                                          namespaces=self.ns2)[0].text.split()
            except (etree.Error, IndexError) as e:
                logger.warning("unable to read corners SW and NE: %s" % e)
                return

        try:
            self._sw = [float(c) for c in ret[0].split(',')]
            self._ne = [float(c) for c in ret[1].split(',')]

        except (ValueError, IndexError) as e:
            logger.warning("unable to read corners SW and NE: %s" % e)
            return

    def _read_wkt_prj(self) -> None:
        """ attempts to read the WKT projection string """

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                      'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the WKT projection string: %s" % e)
            return

        if len(ret) == 0:
            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/referenceSystemInfo/smXML:MD_CRS',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the WKT projection string: %s" % e)
                return

            if len(ret) != 0:
                logger.warning("unsupported method to describe CRS")
                # noinspection PyUnresolvedReferences
                self._xml_srs = etree.tostring(ret[0], pretty_print=True)
                # print(self._xml_srs)
                return

        try:
            space = self.xml_tree.xpath(
                '//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString',
                namespaces=self.ns)
            # logger.info("codeSpace: %s" % space[0].text)

            if space[0].text == "EPSG":
                self._wkt_srs_epsg_code = int(ret[0].text)
                sr = osr.SpatialReference()
                sr.ImportFromEPSG(self.wkt_srs_epsg_code)
                self._wkt_srs = sr.ExportToWkt()
            else:
                self._wkt_srs_epsg_code = None
                self._wkt_srs = ret[0].text

        except (ValueError, IndexError) as e:
            logger.warning("unable to read the WKT projection string: %s" % e)
            return

    def _read_wkt_vertical_datum(self) -> None:
        """ attempts to read the WKT vertical datum string """

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                      'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the WKT vertical datum string: %s" % e)
            return

        if len(ret) == 0:
            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/referenceSystemInfo/smXML:MD_CRS',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the WKT vertical datum string: %s" % e)
                return

            if len(ret) != 0:
                logger.warning("unsupported method to describe Vertical Datum")
                # noinspection PyUnresolvedReferences
                self._xml_vertical_datum = etree.tostring(ret[0], pretty_print=True)
                # print(self.xml_vertical_datum)
                return

        try:
            space = self.xml_tree.xpath(
                '//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString',
                namespaces=self.ns)
            # logger.info("codeSpace: %s" % space[0].text)

            if space[1].text == "EPSG":
                self._wkt_vertical_datum_epsg_code = int(ret[1].text)
                sr = osr.SpatialReference()
                sr.ImportFromEPSG(self.wkt_vertical_datum_epsg_code)
                self._wkt_vertical_datum = sr.ExportToWkt()
            else:
                self._wkt_vertical_datum_epsg_code = None
                self._wkt_vertical_datum = ret[1].text

        except (ValueError, IndexError) as e:
            logger.warning("unable to read the WKT vertical datum string: %s" % e)
            return

    def _read_bbox(self) -> None:
        """ attempts to read the bounding box values """

        # noinspection PyUnresolvedReferences
        try:
            ret_x_min = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal',
                                            namespaces=self.ns)
            ret_x_max = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal',
                                            namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the bbox's longitude values: %s" % e)
            return

        if len(ret_x_min) == 0:
            # noinspection PyUnresolvedReferences
            try:
                ret_x_min = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/westBoundLongitude',
                                                namespaces=self.ns2)
                ret_x_max = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/eastBoundLongitude',
                                                namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the bbox's longitude values: %s" % e)
                return

        try:
            self._lon_min = float(ret_x_min[0].text)
            self._lon_max = float(ret_x_max[0].text)
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the bbox's longitude values: %s" % e)
            return

        # noinspection PyUnresolvedReferences
        try:
            ret_y_min = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal',
                                            namespaces=self.ns)
            ret_y_max = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal',
                                            namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the bbox's latitude values: %s" % e)
            return

        if len(ret_y_min) == 0:

            # noinspection PyUnresolvedReferences
            try:
                ret_y_min = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/southBoundLatitude',
                                                namespaces=self.ns2)
                ret_y_max = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/northBoundLatitude',
                                                namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the bbox's latitude values: %s" % e)
                return

        try:
            self._lat_min = float(ret_y_min[0].text)
            self._lat_max = float(ret_y_max[0].text)
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the bbox's latitude values: %s" % e)
            return

    def _read_abstract(self) -> None:
        """ attempts to read the abstract string """

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/gmd:abstract/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the abstract string: %s" % e)
            return

        if len(ret) == 0:
            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/abstract',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the abstract string: %s" % e)
                return

        try:
            self._abstract = ret[0].text
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the abstract string: %s" % e)
            return

    def _read_date(self) -> None:
        """ attempts to read the date string """

        ret = self.xml_tree.xpath('//*/gmd:CI_Date/gmd:date/gco:Date',
                                  namespaces=self.ns)

        if len(ret) == 0:
            ret = self.xml_tree.xpath('//*/smXML:CI_Date/date',
                                      namespaces=self.ns2)

        if len(ret) == 0:
            ret = self.xml_tree.xpath('//*/gmd:dateStamp/gco:Date',
                                      namespaces=self.ns)

        if len(ret) == 0:
            logger.warning("unable to read the date string")

        try:
            text_date = ret[0].text
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the date string: %s" % e)
            return

        tm_date = None
        # noinspection PyBroadException
        try:
            parsed_date = dateutil.parser.parse(text_date)
            tm_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.warning("unable to handle the date string: %s (%s)" % (text_date, e), exc_info=True)

        if tm_date is None:
            self._date = text_date
        else:
            self._date = tm_date

    def _read_survey_start_date(self) -> None:
        """ attempts to read the survey date strings """

        try:
            ret_begin = self.xml_tree.xpath(
                '//*/gmd:identificationInfo/bag:BAG_DataIdentification/gmd:extent/gmd:EX_Extent/'
                'gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition',
                namespaces=self.ns)

            if len(ret_begin) == 0:
                ret_begin = self.xml_tree.xpath(
                    '//*/identificationInfo/smXML:BAG_DataIdentification/extent/smXML:EX_Extent/'
                    'temporalElement/smXML:EX_TemporalExtent/extent/TimePeriod/beginPosition',
                    namespaces=self.ns2)

        except Exception as e:
            logger.warning(e, exc_info=True)
            return

        if len(ret_begin) == 0:
            logger.warning("unable to read the survey begin date string")
            return

        try:
            text_begin_date = ret_begin[0].text
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the survey begin date string: %s" % e)
            return

        tm_begin_date = None
        # noinspection PyBroadException
        try:
            parsed_date = dateutil.parser.parse(text_begin_date)
            tm_begin_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.warning("unable to handle the survey begin date string: %s (%s)" % (text_begin_date, e),
                           exc_info=True)

        if tm_begin_date is None:
            self._survey_start_date = text_begin_date
        else:
            self._survey_start_date = tm_begin_date

        # logger.debug('start: %s' % self.survey_start_date)

    def _read_survey_end_date(self) -> None:
        """ attempts to read the survey date strings """

        try:
            ret_end = self.xml_tree.xpath(
                '//*/gmd:identificationInfo/bag:BAG_DataIdentification/gmd:extent/gmd:EX_Extent/'
                'gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition',
                namespaces=self.ns)

            if len(ret_end) == 0:
                ret_end = self.xml_tree.xpath(
                    '//*/identificationInfo/smXML:BAG_DataIdentification/extent/smXML:EX_Extent/'
                    'temporalElement/smXML:EX_TemporalExtent/extent/TimePeriod/endPosition',
                    namespaces=self.ns2)
        except Exception as e:
            logger.warning(e, exc_info=True)
            return

        if len(ret_end) == 0:
            logger.warning("unable to read the survey end date string")
            return

        try:
            text_end_date = ret_end[0].text
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the survey end date string: %s" % e)
            return

        tm_end_date = None
        # noinspection PyBroadException
        try:
            parsed_date = dateutil.parser.parse(text_end_date)
            tm_end_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            logger.warning("unable to handle the survey end date string: %s (%s)" % (text_end_date, e), exc_info=True)

        if tm_end_date is None:
            self._survey_end_date = text_end_date
        else:
            self._survey_end_date = tm_end_date

        # logger.debug('end: %s' % self.survey_end_date)

    def _read_uncertainty_type(self) -> None:
        """ attempts to read the uncertainty type """
        old_format = False

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath('//*/bag:verticalUncertaintyType/bag:BAG_VertUncertCode/@codeListValue',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the uncertainty type string: %s" % e)
            return

        if len(ret) == 0:

            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/verticalUncertaintyType',
                                          namespaces=self.ns2)
                old_format = True
            except etree.Error as e:
                logger.warning("unable to read the uncertainty type string: %s" % e)
                return

        try:
            if old_format:
                self._unc_type = ret[0].text
            else:
                self._unc_type = ret[0]
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the uncertainty type attribute: %s" % e)
            return

    def _read_security_constraints(self) -> None:
        """ attempts to read the uncertainty type """
        old_format = False

        # noinspection PyUnresolvedReferences
        try:
            ret = self.xml_tree.xpath(
                '//*/gmd:MD_SecurityConstraints/gmd:classification/gmd:MD_ClassificationCode/@codeListValue',
                namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the uncertainty type string: %s" % e)
            return

        if len(ret) == 0:

            # noinspection PyUnresolvedReferences
            try:
                ret = self.xml_tree.xpath('//*/smXML:MD_SecurityConstraints/classification',
                                          namespaces=self.ns2)
                old_format = True
            except etree.Error as e:
                logger.warning("unable to read the uncertainty type string: %s" % e)
                return

        try:
            if old_format:
                self._sec_constr = ret[0].text
            else:
                self._sec_constr = ret[0]
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the uncertainty type attribute: %s" % e)
            return
