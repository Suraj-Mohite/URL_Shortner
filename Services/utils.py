import random, string
import logging
import sys

logger = logging.getLogger(__name__)

def get_alias():
    try:
        return "".join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(10)])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("get_alias %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Services'})
        return None
