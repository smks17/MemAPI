import logging

from .sql import models, engine
from .config import settings

models.Base.metadata.create_all(bind=engine)

logging_level = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(level=logging_level)
