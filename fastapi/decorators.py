import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def log_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Ejecutando: {func.__name__}")
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        logger.info(f"{func.__name__} tardó {fin - inicio:.3f} segundos")
        return resultado
    return wrapper
