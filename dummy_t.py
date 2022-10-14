#Dummy trombone for testing
import asyncio
import time

def set_trombone_delay(address, val, overshoot, use_cal_table, callback):
    print(f"Setting trombone {address} to {val:,}")
    time.sleep(.1)
    callback(1)
    return