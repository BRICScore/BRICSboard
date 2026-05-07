from gpiozero import LED
import asyncio

class BRVLedController:
    def __init__:
        self.on_led = LED(22)           # connected to GPIO22
        self.bluetooth_led = LED(17)    # connected to GPIO17
        self.serial_led = LED(27)       # connected to GPIO27
        self.led_map = [ 1, 0, 0 ]
        self.size = 3

        asyncio.run(self.main_loop())
    
    def get_led_map(self):
        return self.led_map
    
    def set_led_map(self, new_map):
        if len(map) != self.size:
            return
        self.led_map = new_map
    
    async def main_loop(self):
        if self.led_map[0] == 1:
            self.on_led.on()
        if self.led_map[1] == 1:
            self.bluetooth_led.on()
        if self.led_map[2] == 1:
            self.serial_led.on()
        
        await asyncio.sleep(0.5)

        self.on_led.off()
        self.bluetooth_led.off()
        self.serial_led.off()
    
