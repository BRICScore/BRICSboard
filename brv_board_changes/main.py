# TODO: Maybe try an change from threads to subprocesses
# Example:
# python main.py -i file -if input_file.jsonl
import time
import argparse

from pathlib import Path
from threading import Thread

from Driver.data_readers.middleware import MiddlewareBoardDataReader
from data_readers.file import FileReader
from data_savers.jsonl import JsonlDataSaver
from data_readers.com_port import ComPortDataReader
from data_analyzers.data_plotter import DataPlotter
from data_readers.bluetooth import BluetoothDataReader
from data_parsers.default_data_parser import DefaultDataParser

def check_output_file_status(output_filepath):
    overwrite = True
    if not output_filepath.suffix == '.jsonl':
        print('Output file must be in JSONL format')
        exit(1)
    if output_filepath.exists():
        print('Output file already exists. Do you want to: (1) overwrite or (2) append?')
        while True:
            option = input('Enter option: ')
            if option == '1':
                output_filepath.unlink()
                overwrite = True
                break
            elif option == '2':
                overwrite = False
                break
            else:
                print('Invalid option')
    return overwrite

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Breathing Rhythm Analyzer')
    parser.add_argument('-i', '--input', choices=['bt', 'usb', 'file', 'mid'], required=True, help='Input source: bt (Bluetooth), usb (USB), file (File), or mid (middleware board)')
    parser.add_argument('-if', '--inputfile', type=str, help='File path if input is file. JSONL format')
    parser.add_argument('-of', '--outputfile', type=str, help='File path to save data. JSONL format. If not provided, data is not saved')
    parser.add_argument('-np', '--noplot', action='store_true', help='Do not plot data. By default, data is plotted')
    parser.add_argument('-ss', '--skipsleep', action='store_true', help='Do not add sleeps between data points in file input mode. By default, data is sent with real intervals')
    parser.add_argument('-v2', '--version2', action='store_true', help='Use version 2 of the device')

    args = parser.parse_args()

    # Validate input type
    thread_input = None
    if args.input == "bt":
        thread_input = Thread(target=BluetoothDataReader, args=(f"BRV{"2" if args.version2 else ""}",))
    elif args.input == "mid":
        thread_input = Thread(target=MiddlewareBoardDataReader, args=(f"BRV{"2" if args.version2 else ""}",))
    elif args.input == "usb":
        thread_input = Thread(target=ComPortDataReader, args=(f"BRV{"2" if args.version2 else ""}",))
    elif args.input == "file":
        if args.inputfile is None:
            print("Input file is required for file input")
            exit(1)
        input_filepath = Path(args.inputfile)
        if not input_filepath.exists():
            print("Input file does not exist")
            exit(1)
        if not input_filepath.suffix == ".jsonl":
            print("Input file must be in JSONL format")
            exit(1)
        thread_input = Thread(target=FileReader, args=(input_filepath, args.skipsleep))
    thread_input.daemon = True

    # Validate output file
    thread_data_saver = None

    if args.outputfile is not None:
        output_filepath = Path(args.outputfile)
        overwrite = check_output_file_status(output_filepath)
        thread_data_saver = Thread(target=JsonlDataSaver, args=(output_filepath, overwrite))
        thread_data_saver.daemon = True

    thread_data_parser = Thread(target=DefaultDataParser)
    thread_data_parser.daemon = True

    thread_plotter = None
    if not args.noplot:
        thread_plotter = Thread(target=DataPlotter)
        thread_plotter.daemon = True

    # Start all threads
    if thread_plotter is not None:
        thread_plotter.start()
    if thread_data_saver is not None:
        thread_data_saver.start()
    thread_data_parser.start()
    thread_input.start()

    while True:
        time.sleep(1)
