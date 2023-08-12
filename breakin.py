import serial
import time
import signal
import sys

serial_port = None

def signal_handler(sig, frame):
    if serial_port:
        serial_port.write(f'pwm 1 0\n'.encode())
        serial_port.write('pwm m 0\r\n'.encode())
    sys.exit(0)

if __name__ == "__main__":
    last_update_time = int(round(time.time() * 1000))
    signal.signal(signal.SIGINT, signal_handler)

    serial_port = serial.Serial(
        port='COM7',
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
    )

    serial_port.write('debug\r\n'.encode())

    serial_port.write('pwm m 1\r\n'.encode())

    power = -14
    serial_port.write(f'pwm 1 {power}\n'.encode())
    time.sleep(2)

    while True:
        # if int(round(time.time() * 1000)) - last_update_time > 4000:
        power = 26
        serial_port.write(f'pwm 1 {power}\n'.encode())
        time.sleep(0.1)
        print(serial_port.read_all())
        power = 14
        serial_port.write(f'pwm 1 {power}\n'.encode())
        time.sleep(1)
        print(serial_port.read_all())

        power = -26
        serial_port.write(f'pwm 1 {power}\n'.encode())
        time.sleep(0.1)
        print(serial_port.read_all())
        power = -14
        serial_port.write(f'pwm 1 {power}\n'.encode())
        time.sleep(1)
        print(serial_port.read_all())