from app.monitoring.logging.logging_startup import logger


class CalculationExceptionError(Exception):
    """When a Class that uses Calculation Method fails,it throws this Exception"""
    def __init__(self, values:list,typ:str):
        message = f"Calculation of Values failed at {typ}: {values}"
        logger.error(message)
        super().__init__(message)