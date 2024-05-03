import argparse
import os
import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag import __version__
from hyo2.bag.bag import BAGFile, is_bag

logger = logging.getLogger(__name__)


def main():
    app_name = "bag_elevation"
    app_info = "Extraction of elevation layer from an OpenNS BAG file, using hyo2.bag r%s" % __version__

    formats = ['ascii', 'geotiff', 'xyz']

    parser = argparse.ArgumentParser(prog=app_name, description=app_info)
    parser.add_argument("bag_file", type=str, help="a valid BAG file from which to extract metadata")
    parser.add_argument("-f", "--format", help="one of the available file format: " + ", ".join(formats),
                        choices=formats, default="geotiff", metavar='')
    parser.add_argument("-o", "--output", help="the output file", type=str)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        set_logging(ns_list=['hyo2.bag'])
        logger.debug("> verbosity: ON")

        logger.debug("> input: %s" % args.bag_file)

        if args.output:
            args.output = os.path.abspath(args.output)
            logger.debug("> output: %s" % args.output)
        else:
            args.output = None
            logger.debug("> output: [default]")

        logger.debug("> format: %s" % args.format)

    if not os.path.exists(args.bag_file):
        parser.exit(1, "ERROR: the input valid does not exist: %s" % args.bag_file)

    if not is_bag(args.bag_file):
        parser.exit(1, "ERROR: the input valid does not seem a BAG file: %s" % args.bag_file)

    bf = BAGFile(args.bag_file, mode='r')
    bag_meta = None
    try:
        bag_meta = bf.populate_metadata()
    except Exception as e:
        parser.exit(1, "ERROR: issue in metadata population: %s" % e)
    bag_elevation = None
    try:
        bag_elevation = bf.elevation(mask_nan=False)
    except Exception as e:
        parser.exit(1, "ERROR: issue in elevation population: %s" % e)

    try:
        from hyo2.bag.elevation import Elevation2Gdal
        Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt=args.format, out_file=args.output)
    except Exception as e:
        parser.exit(1, "ERROR: issue in output creation: %s" % e)

    if args.verbose:
        logger.debug("> DONE")


if __name__ == "__main__":
    main()
