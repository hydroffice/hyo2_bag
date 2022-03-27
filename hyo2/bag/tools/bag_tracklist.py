import os
import logging
import argparse

from hyo2.abc.lib.logging import set_logging
from hyo2.bag import __version__
from hyo2.bag.bag import BAGFile, is_bag

logger = logging.getLogger(__name__)


def main():
    app_name = "bag_tracklist"
    app_info = "Extraction the tracklist from an OpenNS BAG file, using hyo2.bag r%s" % __version__

    formats = ['csv']

    parser = argparse.ArgumentParser(prog=app_name, description=app_info)
    parser.add_argument("bag_file", type=str, help="a valid BAG file from which to extract metadata")
    parser.add_argument("-f", "--format", help="one of the available file format: " + ", ".join(formats),
                        choices=formats, default="csv", metavar='')
    parser.add_argument("-o", "--output", help="the output file", type=str)
    parser.add_argument("-hd", "--header", help="add an header", action="store_true")
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
        logger.debug("> header: %s" % args.header)

    if not os.path.exists(args.bag_file):
        parser.exit(1, "ERROR: the input valid does not exist: %s" % args.bag_file)

    if not is_bag(args.bag_file):
        parser.exit(1, "ERROR: the input valid does not seem a BAG file: %s" % args.bag_file)

    bf = BAGFile(args.bag_file, mode='r')
    tl = None
    try:
        tl = bf.tracking_list()
    except Exception as e:
        parser.exit(1, "ERROR: issue in tracking-list recovery: %s" % e)

    tlf = ""
    if args.header:
        try:
            tlf = bf.tracking_list_fields()
        except Exception as e:
            parser.exit(1, "ERROR: issue in tracking-list fields recovery: %s" % e)

    try:
        from hyo2.bag.tracklist import TrackList2Csv
        TrackList2Csv(track_list=tl, csv_file=args.output, header=tlf)
    except Exception as e:
        parser.exit(1, "ERROR: issue in output creation: %s" % e)

    if args.verbose:
        logger.debug("> DONE")


if __name__ == "__main__":
    main()
