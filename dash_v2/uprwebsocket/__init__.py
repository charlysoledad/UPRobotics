import logging

logger = logging.getLogger("net2js")

try:
    import tornado
except ImportError as e:
    logger.info(e)
    logger.info("Could not import tornado, disabling support.")
else:
    from .tornado_handlers import (
        WSHandler,
        NonCachingStaticFileHandler
    )