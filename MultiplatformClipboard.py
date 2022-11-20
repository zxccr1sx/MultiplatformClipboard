import socket, threading
import pywebio
from pywebio import *
from pywebio.input import *
from pywebio import start_server 
import webbrowser

import socket, threading
import pyperclip


connections = []

def handle_user_connection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                broadcast(msg_to_send, connection)
                pyperclip.copy(msg.decode())

            else:
                remove_connection(connection)
                break

        except Exception as e:
            remove_connection(connection)
            break


def broadcast(message: str, connection: socket.socket) -> None:


    for client_conn in connections:
        if client_conn != connection:
            try:
                client_conn.send(message.encode())

            except Exception as e:
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:
    if conn in connections:
        conn.close()
        connections.remove(conn)


def server() -> None:

    LISTENING_PORT = 4949
    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)
        
        while True:
            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()
            


    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()



    

def handle_messages(connection: socket.socket):

    while True:
        try:
            msg = connection.recv(1024)
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            connection.close()
            break

def client() -> None:

    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 4949

    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        threading.Thread(target=handle_messages, args=[socket_instance]).start()


        while True:
            msg = input("Enter text", type=TEXT)

            if msg == 'quit':
                break


            socket_instance.send(msg.encode())


        socket_instance.close()

    except Exception as e:
        socket_instance.close()

webbrowser.open('http://192.168.0.106/?app=server')

if __name__ == "__main__":
    start_server([server, client], port=80)