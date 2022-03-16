import pyb


def main():
    serial = pyb.USB_VCP()

    while True:
        if serial.any():
            bytes_in = serial.readline()
        else:
            pyb.delay(50)


if __name__ == "__main__":
    main()