# =========================================================================
#           VNA Calibration Device Instrument Simulation
#           By Dylan Fleming, 45313345
# =========================================================================

# Imports
import pyvisa
import pyvisa_sim
import os
import socket


def start_simulated_instrument():
    """
    start_simulated_instrument initiates the simulated instrument, including opening the socket connection and
    :return: NULL
    """
    rm = pyvisa.ResourceManager('C:/Users/dylan/Documents/Thesis - Python/Thesis - Calibration/instrument.yaml@sim')
    print(rm.list_resources())
    instrument = rm.open_resource('ASRL1::INSTR')

    # Setup TCP/IP server for communication
    host = '127.0.0.1'
    port = 5025
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received command: {data}")
                # Respond with simulated data or acknowledge the command
                response = f"Simulated response to {data}"
                client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        instrument.close()
        server_socket.close()
        print("Instrument connection closed.")


if __name__ == "__main__":
    start_simulated_instrument()


