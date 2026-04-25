## Middleware board for optimal communication between BRV board and data decoding program. ##

In order to use the middleware board
1. Files in the `brv_changes_folder` should be added to the program used for recieving data from the BRV.
2. Middleware board should be turned on and **DISCONNECTED** from the BRV vest.
3. Data processing program should be started with the following command:

   `python main.py -i mid -of "name_of_output_file.jsonl"`
4. After the middleware program loads and the data processing program prints out "Connected" you can connect the middleware board to BRV vest and data should start coming through
5. After finishing measuring data with BRV unplug it from the middleware board, but **do not**
terminate the program running on the board until its queue has been cleared - it can lead to
significant data loss. The end of the queue is signaled by lack of arriving data packets from the midlleware board visible in the data receiving program.
6. Afterwards you can safely unplug the middleware board and close the data receiving program.

Autoload should take around 5 minutes to start.

If the autoload function fails to load the board should be used in the following way:
1. Files in the `brv_changes_folder` should be added to the program used for recieving data from the BRV.
2. Plug in the raspberry pi and make sure it is **connected to the internet** and the cable
connecting it to BRV is unplugged.
3. After boot connect to it using ssh and execute following commands:
    - `ls brv_board/test/env/`
    - `source bin/activate`
    - `python main.py`
4. When communicates visible in console inform you that the bluetooth server is registered
you can run the brv data processing program with a following command:

   `python main.py -i mid -of "name_of_output_file.jsonl"`
5. After the data processing program prints that it has connected to BRV you can plug the BRV
vest into the middleware board. 
6. After finishing measuring data with BRV unplug it from the middleware board, but **do not**
terminate the program running on the board until its queue has been cleared - it can lead to
significant data loss.
7. Afterwards you can safely unplug the middleware board and close the data receiving program.
