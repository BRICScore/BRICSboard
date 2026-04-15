from BRVSerialConnection import BRVSerialConnection
from BRVBluetoothServer import BRVBluetoothServer
from BRVDataService import BRVDataService
import asyncio
from threading import Thread
import time
import sys

async def waiter():
    await asyncio.sleep(1)

service = BRVDataService()

filename = None
if len(sys.argv) > 1:
    filename = sys.argv[1]

serial_thread = Thread(target=BRVSerialConnection, args=(service, filename))
serial_thread.daemon = True
bluetooth_thread = Thread(target=BRVBluetoothServer, args = (service, True))
bluetooth_thread.daemon = True

print("BRV: starting threads")

serial_thread.start()
bluetooth_thread.start()

while True:
    asyncio.run(waiter())
