# Code for VNA.py

import argparse
import logging
import sys
from time import sleep
from PyQt5 import QtWidgets

from NanoVNASaver.About import version, INFO
from NanoVNASaver.NanoVNASaver import NanoVNASaver
from NanoVNASaver.Touchstone import Touchstone

from NanoVNASaver.Hardware.Hardware import Interface, get_interfaces, get_VNA
from NanoVNASaver.Controls.Control import Control

# Code for LED
import wiringpi
import time

OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0
LED_GRN = 29
LED_RED = 28
LED_YLW = 27
BTN_PIN = 3

wiringpi.wiringPiSetup()
wiringpi.pinMode(LED_GRN, OUTPUT)
wiringpi.pinMode(LED_RED, OUTPUT)
wiringpi.pinMode(LED_YLW, OUTPUT)
wiringpi.pinMode(BTN_PIN, INPUT)

def main():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Set loglevel to debug"
    )
    parser.add_argument(
        "-D", "--debug-file", help="File to write debug logging output to"
    )
    parser.add_argument(
        "-a", "--auto-connect", action="store_true", help="Auto connect if one device detected"
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Touchstone file to load as sweep for off" " device usage",
    )
    parser.add_argument(
        "-r",
        "--ref-file",
        help="Touchstone file to load as reference for off" " device usage",
    )
    parser.add_argument(
        "--version", action="version", version=f"NanoVNASaver {version}"
    )
    args = parser.parse_args()

    console_log_level = logging.WARNING
    file_log_level = logging.DEBUG

    print(INFO)

    if args.debug:
        console_log_level = logging.DEBUG

    logger = logging.getLogger("NanoVNASaver")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if args.debug_file:
        fh = logging.FileHandler(args.debug_file)
        fh.setLevel(file_log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    logger.info("Startup...")

    app = QtWidgets.QApplication(sys.argv)

    print("Device is Ready")
    wiringpi.digitalWrite(LED_GRN, LOW)
    wiringpi.digitalWrite(LED_RED, LOW)
    wiringpi.digitalWrite(LED_YLW, HIGH)

    while(True):
        # if wiringpi.digitalRead(BTN_PIN) == HIGH:
        if (True):
            window = NanoVNASaver()
            wiringpi.digitalWrite(LED_YLW, LOW)
            window.establishSerial()
            window.performCalibration()
            # window.show()

            # if args.auto_connect:
            #     window.auto_connect()
            if args.file:
                t = Touchstone(args.file)
                t.load()
                window.saveData(t.s11, t.s21, args.file)
                window.dataUpdated()
            if args.ref_file:
                t = Touchstone(args.ref_file)
                t.load()
                window.setReference(t.s11, t.s21, args.ref_file)
                window.dataUpdated()
            try:
                print("point c")
                app.exec()
            except BaseException as exc:
                logger.exception("%s", exc)
                raise exec

if __name__ == "__main__":
    main()
