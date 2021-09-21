import os
import logging
import argparse

from hyo2.abc.lib.logging import set_logging
from hyo2.bag import __version__
from hyo2.bag.bag import BAGFile, is_bag

logger = logging.getLogger(__name__)


def main():
    app_name = "bag_metadata"
    app_info = "Extraction of XML metadata from an OpenNS BAG file, using hyo2.bag r%s" % __version__

    parser = argparse.ArgumentParser(prog=app_name, description=app_info)
    parser.add_argument("bag_file", type=str, help="a valid BAG file from which to extract metadata")
    parser.add_argument("-x", "--xml_file", help="the output XML metadata file", type=str)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        set_logging(ns_list=['hyo2.bag'])
        logger.debug("> verbosity: ON")

        logger.debug("> input: %s" % args.bag_file)

        if args.xml_file:
            args.xml_file = os.path.abspath(args.xml_file)
            logger.debug("> output: %s" % args.xml_file)
        else:
            args.xml_file = os.path.abspath(BAGFile.default_metadata_file)
            logger.debug("> output: %s [default]" % args.xml_file)

    if not os.path.exists(args.bag_file):
        parser.exit(1, "ERROR: the input valid does not exist: %s" % args.bag_file)

    if not is_bag(args.bag_file):
        parser.exit(1, "ERROR: the input valid does not seem a BAG file: %s" % args.bag_file)

    bf = BAGFile(args.bag_file)
    try:
        bf.extract_metadata(args.xml_file)
    except Exception as e:
        parser.exit(1, "ERROR: %s" % e)

    if args.verbose:
        logger.debug("> DONE")


if __name__ == "__main__":
    main()
