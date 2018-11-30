import socket
import sys
import threading

from database_methods import DatabaseConnector

connector = DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    IP_address = '0.0.0.0'
    Port = 5050
else:
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(10)
print('\n\tServer started: ', server)
dict_of_users = {}

HELP = '''\nHelp : /h - help | /l -login | /t - show last 10 | /u - show active users | /x - exit '''
BANNER = '''\n\tWelcome to this chatroom!
\tYou should login (or register) for chat and use some commands '''


def clientthread(conn, addr):
    message2conn(BANNER + HELP, conn)
    while True:
        user = dict_of_users.get(conn, 'GUEST')
        try:
            message = conn.recv(2048)
            message = message.decode().strip()

            if message == '/h':
                message_to_send = 'You are logged as: ' + user + '@' + addr[0] + "> " + HELP
                message2conn(message_to_send, conn)
            elif message == '/x':
                message2conn('Bye. Good Luck!', conn)
                remove(conn)
            elif message == '/l':
                login(conn)
            elif message == '/u' and user != 'GUEST':
                message = 'Users: ' + ', '.join([i for i in dict_of_users.values() if i != 'GUEST'])
                message2conn(message if message else 'None', conn)
            elif message == '/t' and user != 'GUEST':
                posts2conn(connector.tail_posts(), conn)
            elif message:
                message = user + '@' + addr[0] + "> " + message
                print(message)
                message_to_send = user + '@' + addr[0] + "> " + message
                broadcast(message_to_send.encode(), conn)
                if user != 'GUEST':
                    connector.save_post(user, message)


            else:
                remove(conn)
        except:
            continue


def broadcast(message, conn):
    for user_connection in dict_of_users:
        user_name = dict_of_users[conn]
        if user_connection != conn:
            try:
                user_connection.send(message)
            except:
                user_connection.close()
                del dict_of_users[user_connection]


def posts2conn(posts, conn):
    if not posts:
        message2conn('\nLog empty\n', conn)
    else:
        for post in posts:
            message = '\t'.join([str(i) for i in post]) + '\n'
            message2conn(message, conn)


def message2conn(message, conn):
    try:
        conn.send(message.encode())
    except:
        conn.close()
        remove(conn)


def login(conn):
    message2conn('Enter your name : ', conn)
    try:
        name = conn.recv(2048)
        name = name.decode().strip()
        if 2 < len(name) < 20 and name not in dict_of_users:
            message2conn('Enter your password: ', conn)
            try:
                password = conn.recv(2048)
                password = password.decode().strip()
            except:
                message2conn('You are not logged', conn)
                return False
            if connector.is_username_used(name):
                if connector.check_user(name, password):
                    message = 'Thank you, {}. You are logged!'.format(name)
                else:
                    message2conn('Password is wrong', conn)
                    return False
            else:
                if connector.create_user(name, password):
                    message = 'Thank you, {}. You are registered and logged!'.format(name)
                else:
                    message2conn('Login or password are wrong', conn)
                    return False
            dict_of_users[conn] = name
            message2conn(message, conn)
            return True
        else:
            message2conn('This name is not available!\n\t( 2 < len(NAME) < 20 )', conn)
            return False
    except:
        message2conn('You are not logged', conn)
        return False


def remove(conn):
    if conn in dict_of_users:
        del dict_of_users[conn]


while True:
    connect, addr = server.accept()

    dict_of_users[connect] = 'GUEST'
    print(addr[0] + " connected as GUEST")

    th = threading.Thread(target=clientthread, args=(connect, addr))
    th.start()

connect.close()
server.close()