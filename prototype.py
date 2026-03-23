import zmq
import json
import serial
import os
import serial.tools.list_ports

BRA_OUTPUT_STRUCT_SIZE_BYTES = 94

pids = { "BRV": 5741,
         "BRV2": 5742}

name = "BRV2"

class BRVConnectionEnhancer:
    def __init__( self ):
        context = zmq.Context()
        usb_socket = context.socket(zmq.PUB)
        usb_socket.bind("tcp://*:5555")

        self.name = name                        # brv board name
        self.backup_file_name = getBackupFileName()

        while True:
            try:
                print("BRICS board: Looking for {name}...")
                while True:
                    ports = self.findBra()
                    if len(ports) > 0:
                        print(f"BRICS board: found {name} at port: ", ports[0])
                        bra_port = ports[0]
                        break
                    print("BRICS board: connecting to {name}...")
                    with serial.Serial(bra_port, 115200, timeout=1) as ser:
                        print("BRICS board: connected")
                        while True:
                            data = ser.read(BRA_OUTPUT_STRUCT_SIZE_BYTES)
                            if data:
                                # backuping read data
                                with open(self.backup_file_name, "ab") as backup_file:
                                    backup_file.write(data)
                                
                                # todo:
                                # establishing bluetooth connection
                                # sending packets
                            else:
                                print("BRICS board: no data recieved from {name}")
                                continue
            except serial.SerialException as e:
                print("USB connection problem")
    
    def findBra(self):
        ports = list(serial.tools.list_ports.comports())

        resultPorts = []
        for port in ports:
            if port.vid == 483 and port.pid == pids[self.name]:
                resultPorts.append(port.device)
        
        return resultPorts
    
    def getBackupFileName(self):
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
        return result + name


if __name__ == "__main__":
    BRVConnectionEnhancer()
