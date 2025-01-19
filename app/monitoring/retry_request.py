import time

from venv import logger


def retry_request(func, max_retries=2, retry_delay=5, *args, **kwargs):
    attempt = 0
    while attempt < max_retries:
        try:
            result = func(*args, **kwargs)  # Execute the function
            return result  # Return result if successful
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            attempt += 1
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

    logger.error(f"All {max_retries} retries failed.")
    raise Exception(f"Failed after {max_retries} attempts.")



