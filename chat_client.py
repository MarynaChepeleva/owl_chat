import sys
import select
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
COMMANDS = {'/h', '/l', '/x', '/u', '/t', }

if len(sys.argv) != 3:
    IP_address = '0.0.0.0'
    Port = 5050
else:
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])

server.connect((IP_address, Port))
chat = True

while chat:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socket in read_sockets:
        if socket == server:
            message = socket.recv(2048).decode()
            if not message:
                chat = False
                print('Server closed. Bye.')
                break
            sys.stdout.write(message)
            sys.stdout.write('\n ')
            sys.stdout.flush()
            if message.strip().startswith('Bye.'):
                chat = False
                break
        else:
            message = sys.stdin.readline()
            if not message =='\n':
                server.send(message.encode())
server.close()