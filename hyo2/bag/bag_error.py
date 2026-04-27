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
