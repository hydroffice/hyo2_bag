import logging
import dateutil.parser
from lxml import etree
from osgeo import osr
from hyo2.abc2.lib.gdal_aux import GdalAux
from hyo2.bag.helper import Helper

logger = logging.getLogger(__name__)


class Meta:
    """ Helper class to manage BAG xml metadata. """

    ns = {
        'bag': 'http://www.opennavsurf.org/schema/bag',
        'gco': 'http://www.isotc211.org/2005/gco',
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gmi': 'http://www.isotc211.org/2005/gmi',
        'gml': 'http://www.opengis.net/gml/3.2',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    }

    ns2 = {
        'gml': 'http://www.opengis.net/gml',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'smXML': 'http://metadata.dgiwg.org/smXML',
    }

    def __init__(self, meta_xml: bytes | str) -> None:
        GdalAux.push_gdal_error_handler()

        self.xml_tree = etree.fromstring(meta_xml)

        # rows and cols
        self.rows: int | None = None
        self.cols: int | None = None
        self._read_rows_and_cols()

        # resolution along x and y axes
        self.res_x: float | None = None
        self.res_y: float | None = None
        self._read_res_x_and_y()

        # corner SW and NE
        self.sw: list[float] | None = None
        self.ne: list[float] | None = None
        self._read_corners_sw_and_ne()

        # wkt projection
        self.wkt_srs: str | None = None
        self.xml_srs: str | None = None
        self.wkt_srs_epsg_code: str | None = None
        self._read_wkt_prj()

        # wkt vertical datum
        self.wkt_vertical_datum: str | None = None
        self.xml_vertical_datum: str | None = None
        self.wkt_vertical_datum_epsg_code: str | None = None
        self._read_wkt_vertical_datum()

        # bbox
        self.lon_min: float | None = None
        self.lon_max: float | None = None
        self.lat_min: float | None = None
        self.lat_max: float | None = None
        self._read_bbox()

        # abstract
        self.abstract = None
        self._read_abstract()

        # date
        self.date = None
        self._read_date()

        # survey dates
        self.survey_start_date = None
        self._read_survey_start_date()
        self.survey_end_date = None
        self._read_survey_end_date()

        # uncertainty type
        self.unc_type = None
        self._read_uncertainty_type()

        # uncertainty type
        self.sec_constr = None
        self._read_security_constraints()

    def __str__(self) -> str:
        output = "<metadata>"

        if (self.rows is not None) and (self.cols is not None):
            output += "\n    <shape rows=%d, cols=%d>" % (self.rows, self.cols)

        if (self.res_x is not None) and (self.res_y is not None):
            output += "\n    <resolution x=%f, y=%f>" % (self.res_x, self.res_y)

        if (self.sw is not None) and (self.ne is not None):
            output += "\n    <corners SW=%s, NE=%s>" % (self.sw, self.ne)

        if self.wkt_srs is not None:
            output += "\n    <projection=%s>" % Helper.elide(self.wkt_srs, max_len=60)

        if self.date is not None:
            output += "\n    <date=%s>" % self.date

        if self.abstract is not None:
            output += "\n    <abstract=%s>" % self.abstract

        output += "\n    <bbox>"
        if (self.lon_min is not None) and (self.lon_max is not None):
            output += "\n        <x min=%s, max=%s>" % (self.lon_min, self.lon_max)
        if (self.lat_min is not None) and (self.lat_max is not None):
            output += "\n        <y min=%s, max=%s>" % (self.lat_min, self.lat_max)

        if self.unc_type is not None:
            output += "\n    <uncertainty type=%s>" % self.unc_type

        if self.sec_constr is not None:
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

        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:dimensionSize/gco:Integer',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read rows and cols: %s" % e)
            return

        if len(ret) == 0:

            try:
                ret = self.xml_tree.xpath('//*/spatialRepresentationInfo/smXML:MD_Georectified/'
                                          'axisDimensionProperties/smXML:MD_Dimension/dimensionSize',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read rows and cols: %s" % e)
                return

        try:
            self.rows = int(ret[0].text)
            self.cols = int(ret[1].text)

        except (ValueError, IndexError) as e:
            logger.warning("unable to read rows and cols: %s" % e)
            return

    def _read_res_x_and_y(self) -> None:
        """ attempts to read resolution along x- and y- axes """

        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:resolution/gco:Measure',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read res x and y: %s" % e)
            return

        if len(ret) == 0:

            try:
                ret = self.xml_tree.xpath('//*/spatialRepresentationInfo/smXML:MD_Georectified/'
                                          'axisDimensionProperties/smXML:MD_Dimension/resolution/'
                                          'smXML:Measure/smXML:value',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read res x and y: %s" % e)
                return

        try:
            self.res_x = float(ret[0].text)
            self.res_y = float(ret[1].text)

        except (ValueError, IndexError) as e:
            logger.warning("unable to read res x and y: %s" % e)
            return

    def _read_corners_sw_and_ne(self) -> None:
        """ attempts to read corners SW and NE """

        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:cornerPoints/gml:Point/gml:coordinates',
                                      namespaces=self.ns)[0].text.split()
        except (etree.Error, IndexError):
            try:
                ret = self.xml_tree.xpath('//*/spatialRepresentationInfo/smXML:MD_Georectified/'
                                          'cornerPoints/gml:Point/gml:coordinates',
                                          namespaces=self.ns2)[0].text.split()
            except (etree.Error, IndexError) as e:
                logger.warning("unable to read corners SW and NE: %s" % e)
                return

        try:
            self.sw = [float(c) for c in ret[0].split(',')]
            self.ne = [float(c) for c in ret[1].split(',')]

        except (ValueError, IndexError) as e:
            logger.warning("unable to read corners SW and NE: %s" % e)
            return

    def _read_wkt_prj(self) -> None:
        """ attempts to read the WKT projection string """

        try:
            ret = self.xml_tree.xpath('//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                      'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the WKT projection string: %s" % e)
            return

        if len(ret) == 0:
            try:
                ret = self.xml_tree.xpath('//*/referenceSystemInfo/smXML:MD_CRS',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the WKT projection string: %s" % e)
                return

            if len(ret) != 0:
                logger.warning("unsupported method to describe CRS")
                self.xml_srs = etree.tostring(ret[0], pretty_print=True)
                # print(self.xml_srs)
                return

        try:
            space = self.xml_tree.xpath(
                '//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString',
                namespaces=self.ns)
            # logger.info("codeSpace: %s" % space[0].text)

            if space[0].text == "EPSG":
                self.wkt_srs_epsg_code = int(ret[0].text)
                sr = osr.SpatialReference()
                sr.ImportFromEPSG(self.wkt_srs_epsg_code)
                self.wkt_srs = sr.ExportToWkt()
            else:
                self.wkt_srs_epsg_code = None
                self.wkt_srs = ret[0].text

        except (ValueError, IndexError) as e:
            logger.warning("unable to read the WKT projection string: %s" % e)
            return

    def _read_wkt_vertical_datum(self) -> None:
        """ attempts to read the WKT vertical datum string """

        try:
            ret = self.xml_tree.xpath('//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                      'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the WKT vertical datum string: %s" % e)
            return

        if len(ret) == 0:
            try:
                ret = self.xml_tree.xpath('//*/referenceSystemInfo/smXML:MD_CRS',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the WKT vertical datum string: %s" % e)
                return

            if len(ret) != 0:
                logger.warning("unsupported method to describe Vertical Datum")
                self.xml_vertical_datum = etree.tostring(ret[0], pretty_print=True)
                # print(self.xml_vertical_datum)
                return

        try:
            space = self.xml_tree.xpath(
                '//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString',
                namespaces=self.ns)
            # logger.info("codeSpace: %s" % space[0].text)

            if space[1].text == "EPSG":
                self.wkt_vertical_datum_epsg_code = int(ret[1].text)
                sr = osr.SpatialReference()
                sr.ImportFromEPSG(self.wkt_vertical_datum_epsg_code)
                self.wkt_vertical_datum = sr.ExportToWkt()
            else:
                self.wkt_vertical_datum_epsg_code = None
                self.wkt_vertical_datum = ret[1].text

        except (ValueError, IndexError) as e:
            logger.warning("unable to read the WKT vertical datum string: %s" % e)
            return

    def _read_bbox(self) -> None:
        """ attempts to read the bounding box values """

        try:
            ret_x_min = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal',
                                            namespaces=self.ns)
            ret_x_max = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal',
                                            namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the bbox's longitude values: %s" % e)
            return

        if len(ret_x_min) == 0:
            try:
                ret_x_min = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/westBoundLongitude',
                                                namespaces=self.ns2)
                ret_x_max = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/eastBoundLongitude',
                                                namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the bbox's longitude values: %s" % e)
                return

        try:
            self.lon_min = float(ret_x_min[0].text)
            self.lon_max = float(ret_x_max[0].text)
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the bbox's longitude values: %s" % e)
            return

        try:
            ret_y_min = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal',
                                            namespaces=self.ns)
            ret_y_max = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal',
                                            namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the bbox's latitude values: %s" % e)
            return

        if len(ret_y_min) == 0:

            try:
                ret_y_min = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/southBoundLatitude',
                                                namespaces=self.ns2)
                ret_y_max = self.xml_tree.xpath('//*/smXML:EX_GeographicBoundingBox/northBoundLatitude',
                                                namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the bbox's latitude values: %s" % e)
                return

        try:
            self.lat_min = float(ret_y_min[0].text)
            self.lat_max = float(ret_y_max[0].text)
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the bbox's latitude values: %s" % e)
            return

    def _read_abstract(self) -> None:
        """ attempts to read the abstract string """

        try:
            ret = self.xml_tree.xpath('//*/gmd:abstract/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the abstract string: %s" % e)
            return

        if len(ret) == 0:
            try:
                ret = self.xml_tree.xpath('//*/abstract',
                                          namespaces=self.ns2)
            except etree.Error as e:
                logger.warning("unable to read the abstract string: %s" % e)
                return

        try:
            self.abstract = ret[0].text
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
            self.date = text_date
        else:
            self.date = tm_date

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
            self.survey_start_date = text_begin_date
        else:
            self.survey_start_date = tm_begin_date

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
            self.survey_end_date = text_end_date
        else:
            self.survey_end_date = tm_end_date

        # logger.debug('end: %s' % self.survey_end_date)

    def _read_uncertainty_type(self) -> None:
        """ attempts to read the uncertainty type """
        old_format = False

        try:
            ret = self.xml_tree.xpath('//*/bag:verticalUncertaintyType/bag:BAG_VertUncertCode/@codeListValue',
                                      namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the uncertainty type string: %s" % e)
            return

        if len(ret) == 0:

            try:
                ret = self.xml_tree.xpath('//*/verticalUncertaintyType',
                                          namespaces=self.ns2)
                old_format = True
            except etree.Error as e:
                logger.warning("unable to read the uncertainty type string: %s" % e)
                return

        try:
            if old_format:
                self.unc_type = ret[0].text
            else:
                self.unc_type = ret[0]
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the uncertainty type attribute: %s" % e)
            return

    def _read_security_constraints(self) -> None:
        """ attempts to read the uncertainty type """
        old_format = False

        try:
            ret = self.xml_tree.xpath(
                '//*/gmd:MD_SecurityConstraints/gmd:classification/gmd:MD_ClassificationCode/@codeListValue',
                namespaces=self.ns)
        except etree.Error as e:
            logger.warning("unable to read the uncertainty type string: %s" % e)
            return

        if len(ret) == 0:

            try:
                ret = self.xml_tree.xpath('//*/smXML:MD_SecurityConstraints/classification',
                                          namespaces=self.ns2)
                old_format = True
            except etree.Error as e:
                logger.warning("unable to read the uncertainty type string: %s" % e)
                return

        try:
            if old_format:
                self.sec_constr = ret[0].text
            else:
                self.sec_constr = ret[0]
        except (ValueError, IndexError) as e:
            logger.warning("unable to read the uncertainty type attribute: %s" % e)
            return
