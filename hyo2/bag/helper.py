import os
import logging

logger = logging.getLogger(__name__)


class BAGError(Exception):
    """ BAG class for exceptions"""

    def __init__(self, message, *args):
        if isinstance(message, Exception):
            msg = message.args[0] if len(message.args) > 0 else ''
        else:
            msg = message

        self.message = msg
        # allow users initialize misc. arguments as any other builtin Error
        Exception.__init__(self, message, *args)


class Helper(object):
    @classmethod
    def samples_folder(cls):
        samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))
        if not os.path.exists(samples_dir):
            raise BAGError("unable to find the samples folder: %s" % samples_dir)
        return samples_dir

    @classmethod
    def iso19139_folder(cls):
        iso_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "iso19139"))
        if not os.path.exists(iso_dir):
            raise BAGError("unable to find the iso19139 folder: %s" % iso_dir)
        return iso_dir

    @classmethod
    def iso19757_3_folder(cls):
        iso_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "iso19757-3"))
        if not os.path.exists(iso_dir):
            raise BAGError("unable to find the iso19757-3 folder: %s" % iso_dir)
        return iso_dir

    @staticmethod
    def elide(input_str, max_len=255):
        """ only in case the passed string is longer than 'max_len', it applies elision """
        if len(input_str) > max_len:
            return input_str[:max_len] + "[..]"
        return input_str
