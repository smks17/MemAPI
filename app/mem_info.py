import asyncio
import datetime
import logging
import subprocess
from typing import Tuple, Optional

from .config import settings
from .sql import crud, schemas, get_db


PIPE = subprocess.PIPE

def get_mem_usage() -> Optional[Tuple[float, float, float]]:
    """gets the memory usage in POSIX system
    
    Returns
    -------
    Optional[Tuple[float, float, float]]
        If the process is not successful, it will return None. Otherwise, return a tuple with
        three values:
        - The total memory space
        - The amount of memory used
        - The free space 
        All values are in megabytes.
    """
    proc = subprocess.Popen(["free", "-t", "--mega"], stdout=PIPE, stderr=PIPE)
    try:
        outs, errs = proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        logging.error("Getting memory space is killed because of timeout!")
        return None
    if errs != b"":
        print(errs.decode())
        logging.critical("Getting memory space is unavailable!", exc_info=True)
        return None
    outs = outs.decode()
    total, used, free = outs.split()[-3:]
    return total, used, free

async def log_memory_usage():
    while True:
        usage = get_mem_usage()
        if usage:
            total, used, free = usage
            logging.info(f"total: {total} - used: {used} - free: {free}")
            memory_info = schemas.MemCreate(time = datetime.datetime.now(),
                                            free=free,
                                            used=used,
                                            total=total)
            crud.create_memory(get_db(), memory_info)
        # await for some minutes to check memory again
        await asyncio.sleep(settings.delta_time_check_memory.seconds)