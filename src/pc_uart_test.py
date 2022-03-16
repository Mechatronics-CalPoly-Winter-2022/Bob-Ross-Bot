import sys
import serial


def main():
    with serial.Serial('COM4', 115200) as ser:
        ser.write(sys.argv[1].encode())


if __name__ == "__main__":
    main()