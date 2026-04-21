from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
import dbus_fast.aio
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.util import Adapter
import asyncio

BRAOUT_CHAR_UUID = "2137"
BRAOUT_SERV_UUID = "2138"
BRA_OUTPUT_STRUCT_SIZE_BYTES = 94

class BRVDataService(Service):
    def __init__(self):
        super().__init__(BRAOUT_CHAR_UUID, True)

    # function called when reading characteristic - placeholder
    @characteristic(BRAOUT_CHAR_UUID, CharFlags.NOTIFY | CharFlags.READ)
    def brv_characteristic(self):
        pass

    # function called when new brv data
    def update_BRV_value(self, new_BRV_value):
        self.brv_characteristic.changed(new_BRV_value)



