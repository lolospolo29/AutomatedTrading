from app.monitoring.logging.logging_startup import logger

class MappingFailedExceptionError(Exception):
    """Mapping of Object Failed"""
    def __init__(self, mapped_object:str):
        message = f"Mapping of Object Failed: {mapped_object}"
        logger.critical(message)
        super().__init__(message)