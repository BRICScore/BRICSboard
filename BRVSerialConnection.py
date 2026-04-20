import asyncio
import serial
import os
import serial.tools.list_ports
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.util import Adapter
from bluez_peripheral.util import get_message_bus, is_bluez_available
from bluez_peripheral.agent import NoIoAgent

from BRVDataService import BRVDataService

BRA_OUTPUT_STRUCT_SIZE_BYTES = 94

pids = {"BRV": 5741,
        "BRV2": 5742}

name = "BRV"

class BRVSerialConnection:
    def __init__(self, filename, queue):
        self.name = name  # brv board name
        self.backup_file_name = self.getBackupFileName(filename)
        self.is_brv_done = True
        self.queue = queue

        while True:
            try:
                print(f"BRICS serial: Looking for {name}...")
                while True:
                    ports = self.findBra()
                    if len(ports) > 0:
                        print(f"BRICS board serial: found {name} at port: ", ports[0])
                        bra_port = ports[0]
                        break
                with serial.Serial(bra_port, 115200, timeout=1) as ser:
                    print("BRICS board serial: connected")
                    while True:
                        data = ser.read(BRA_OUTPUT_STRUCT_SIZE_BYTES)
                        if data:
                            with open(self.backup_file_name, "ab") as backup_file:
                                backup_file.write(data)
                                # wstawienie do kolejki danych do wyslania
                                self.queue.put(data)
                        else:
                            print(f"BRICS board serial: no data recieved from {name}")
                            continue
            except serial.SerialException as e:
                print("USB connection problem")
                self.is_brv_done = False
                # need to figure this out

    def findBra(self):
        ports = list(serial.tools.list_ports.comports())
        resultPorts = []
        for port in ports:
            if port.vid == 483 and port.pid == pids[self.name]:
                resultPorts.append(port.device)
        return resultPorts

    def getBackupFileName(self, filename):
        name = "data"
        path = os.getcwd()
        if os.name == "nt":
            result = "\\backup\\"
        else:
            result = "/backup/"
        path = path + result
        dir_list = os.listdir(path)
        count = len(dir_list)
        name = name + str(count) + ".txt"
        result = result[1:]
        if filename is not None:
            return result + filename
        f = open(result + name, "x")
        f.close()
        return result + name

if __name__ == "__main__":
    BRVSerial()
