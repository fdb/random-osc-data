import socket
import time
import struct
import random

def create_osc_message(address, value):
    """Create a binary OSC message."""
    # Construct the address string with a null terminator and extra null to make it a multiple of 4 bytes
    address = address.encode('utf-8')
    padded_address = address + b'\x00' * (4 - len(address) % 4)

    # Determine the type tag string, in this case a single float (,f) and pad it as well
    type_tag = b',f\x00\x00'

    # Pack the float value in big-endian format
    binary_value = struct.pack('>f', value)

    # Combine address, type tag, and value into a single message
    return padded_address + type_tag + binary_value

def send_osc_message(host, port, address, value):
    """Send an OSC message to a specific host and port."""
    msg = create_osc_message(address, value)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(msg, (host, port))

# Parameters
HOST = '127.0.0.1'
PORT = 8000
ADDRESS = '/random'

# Send a message every 500ms indefinitely
try:
    while True:
        random_value = random.random() * 100  # Generate a random float between 0 and 100
        send_osc_message(HOST, PORT, ADDRESS, random_value)
        print(f"Sent OSC message with value: {random_value}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopped sending OSC messages.")
