import zmq
import json
import asyncio
from bleak import BleakClient, BleakScanner

from data_containers.bra_output_struct import BraOutputStruct, BRA_OUTPUT_STRUCT_SIZE_BYTES

BRAOUT_CHAR_UUID = "2459"

class MiddlewareBoardDataReader:

    def __init__(self, name: str):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5555")

        self.name = name
        self.semaphore = 0

        asyncio.run(self.start_receiving_data())

    async def start_receiving_data(self):
        while True:
            print(f"Looking for {self.name}...")
            device = await BleakScanner.find_device_by_name(self.name)
            if device is None:
                print(f"Could not find {self.name}. Retrying...")
                continue
            print(f"Found {self.name}. Connecting...")
            async with BleakClient(device) as client:
                print("Connected...")
                await client.start_notify(BRAOUT_CHAR_UUID, self.indication_handler)
                while True:
                    await asyncio.sleep(60)

    def indication_handler(self, characteristic, data):
        if self.semaphore == 0:
            self.half_value = data
            self.semaphore = 1
        else:
            value = data + self.half_value
            #value = value [::-1] #reverse
            data_struct = BraOutputStruct.from_buffer_copy(value)
            self.socket.send_string(json.dumps(data_struct.get_dict()))
            self.semaphore = 0
            print("recieved full package")



if __name__ == "__main__":
    MiddlewareBoardDataReader()
