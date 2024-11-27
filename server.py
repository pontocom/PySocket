import socket

from _thread import *
import threading

print_lock = threading.Lock()


def handle_client(client):
    while True:
        data = client.recv(1024)
        if not data:
            print('Client disconnected')

            print_lock.release()
            break

        data = data[::-1]
        client.send(data)

    client.close()


def server():
    host = socket.gethostname()
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    print("Server running... waiting for connections...")
    server_socket.listen(20)

    while True:
        conn, address = server_socket.accept()
        print_lock.acquire()
        print("Connection from: " + str(address))

        start_new_thread(handle_client, (conn,))

    server_socket.close()


if __name__ == '__main__':
    server()