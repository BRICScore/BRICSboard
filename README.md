#Middleware board for optimal communication between BRV board and data decoding program.#
 
Currently the autoload function is not implemented, so the board should be used in a
follownig order:
1. Plug in the raspberry pi and make sure it is connected to the internet and the cable
connecting it to BRV is unplugged.
2. After boot connect to it using ssh and execute following commands:
    - `ls brv_board/test/env/`
    - `source bin/activate`
    - `python main.py`
3. When communicates visible in console inform you that the bluetooth server is registered
you can run the brv data processing program with a following command:
        `python main.py -i mid -of "name_of_output_file.jsonl"`
4. After the data processing program prints that it has connected to BRV you can plug the BRV
vest into the middleware board. 
5. After finishing measuring data with BRV unplug it from the middleware board, but do not
terminate the program running on the board untill its queue has been cleared - it can lead to
significant data loss. 