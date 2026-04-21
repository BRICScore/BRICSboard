import asyncio
import serial
import os
import serial.tools.list_ports
from Queue import Queue
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.util import Adapter
from bluez_peripheral.util import get_message_bus, is_bluez_available
from bluez_peripheral.agent import NoIoAgent

from BRVDataService import BRVDataService

BRA_OUTPUT_STRUCT_SIZE_BYTES = 94
BRAOUT_CHAR_UUID = "8323"

pids = {"BRV": 5741,
        "BRV2": 5742}

name = "BRV"

class BRVBluetoothServer:
    def __init__(self, service, queue):
        self.name = name  # brv board name
        self.ble_service = service
        self.is_brv_done = True
        self.queue = queue

        asyncio.run(self.register_bluetooth())

    def close_server(self):
        self.is_brv_done = False

    async def register_bluetooth(self):
        print("BRV board bluetooth: Starting registering...")
        bus = await get_message_bus()

        print("BRV board bluetooth: Aquired bus")
        check = await is_bluez_available(bus)
        print("BRV board bluetooth: Bluez check completed")

        adapter = None

        adapter_nodes = (await bus.introspect("org.bluez", "/org/bluez")).nodes
        for node in adapter_nodes:
            if node.name == "hci0":
                introspection = await bus.introspect("org.bluez", "/org/bluez/" + node.name)
                for iface in introspection.interfaces:
                    if iface.name == "org.bluez.Adapter1":
                        proxy = bus.get_proxy_object("org.bluez", "/org/bluez/" + node.name, introspection)
                        adapter = Adapter(proxy)
                        break

        if adapter is not None:
            print("BRV board bluetooth: Adapter iterface found")
        else:
            print("BRV board bluetooth: No necessary adapters, bluetooth is aborting...")
            await bus.wait_for_disconnect()
            print("BRV board bluetooth: Bus disconnected")
            return

        await self.ble_service.register(bus, adapter=adapter)

        print("BRV board bluetooth: Registered bus")

        agent = NoIoAgent()

        # this needs sudo to work - hopefully thats not true
        await agent.register(bus)

        # timeout is set to 60s but can be potentialy be changed
        advert = Advertisement("BRV", [BRAOUT_CHAR_UUID], appearance=0x0340, timeout=60)
        await advert.register(bus, adapter)

        print("BRV board bluetooth: Registering done")

        while self.is_brv_done:
            self.ble_service.update_BRV_value(self.queue.get())
            self.queue.task_done()
            await asyncio.sleep(1)

        await bus.wait_for_disconnect()
        print("BRV board bluetooth: Disconnected")

if __name__ == "__main__":
    BRVBluetoothServer()
