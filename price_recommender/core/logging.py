import typing as t

from loguru import logger


def LogInfo(
    interface: t.Union[t.Dict, t.List, t.Tuple, str, int, bool, None], message: str
):
    """general logger for types and package"""
    logger.debug(message)
    logger.debug("interface content: %s" % interface)
    logger.debug("interface type: %s" % type(interface))
