import logging
import time 
import functools
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger ("TrackerApp")

def log_execution(func):
    @functools.wraps(func)
    async def async_wrapper (*args, **kwargs): 
        logger. info(f"calling '{func.__name__}'")
        start_time = time. time()
        try:
            result = await func(*args, **kwargs) 
            logger. info(f"Method '{func.__name__}' executed successfully.")
            return result
        except Exception as e:
            logger. error (f"Method '{func.__name__}' failed with error: {e}") 
            raise 
        finally:
            end_time = time. time()
            logger.info(f"Method '{func.__name__}' execution time: '{end_time - start_time: .4f}' seconds")
    @functools.wraps(func)
    def sync_wrapper(*args,**kwargs):
        logger.info(f"Calling '{func.__name__}' with args: '{args}' and kwargs: '{kwargs}'")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            logger. info(f"Method '{func.__name__}' executed successfully. ")
            return result
        except Exception as e:
            logger.error(f"Method '{func.__name__}' failed with error: '{e}'") 
            raise
        finally:
            end_time = time.time()
            logger.info(f"Method'{func.__name__}' execution time: '{end_time - start_time: .4f}' seconds")

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper