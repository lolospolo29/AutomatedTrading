from app.monitoring.logging.logging_startup import logger


class CalculationExceptionError(Exception):
    """When a Class that uses Calculation Method fails,it throws this Exception"""
    def __init__(self,typ:str):
        message = f"CalculationExceptionError of Values failed at {typ}"
        logger.error(message)
        super().__init__(message)