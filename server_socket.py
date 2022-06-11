import os
import socket, ssl

def deal_client(stream, newsocket):
    with open('test.xlsx', 'wb') as f:
        while True:
            data = stream.recv(1024)
            f.write(data)
            if not data:
                break
    newsocket.close()

def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    #context.load_cert_chain(certfile='/home/kort/usel-bot/Usel_Bot/cert.pem', keyfile='/home/kort/usel-bot/Usel_Bot/key.pem')
    basedir = os.path.abspath(os.path.dirname(__file__))
    context.load_cert_chain(certfile=f'{basedir}/cert/cert.pem', keyfile=f'{basedir}/cert/key.pem', password='yourpassword')

    bindsocket = socket.socket()
    bindsocket.bind(('127.0.0.1', 10023))
    bindsocket.listen(5)
    print('Server is started!\nAccept new connections')
    while True:
        newsocket, fromaddr = bindsocket.accept()
        print(f'New connection: {newsocket, fromaddr}')
        connstream = context.wrap_socket(newsocket,server_side=True)

        try:
            deal_client(connstream, newsocket)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
