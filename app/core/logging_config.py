from app.core.config import settings
import logging

def configure_logging():
    if settings.ENVIRONMENT not in ["local"]:
        return

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.debug("Logger initialized ✅")

def get_logger(file_name):
    logging.getLogger(file_name)
    return logging.getLogger()
