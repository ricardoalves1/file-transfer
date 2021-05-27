import _thread
import os
import pickle
import socket

server_address = ("localhost", 20000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

clients = []
stop = False

print('Conectado')

def update_screen():
    os.system('cls') or None

    show_clients()
    get_commands()

def show_clients():
    print('Clientes conectados')

    for index, client in enumerate(clients, start = 1):
        print('{} - {}:{}'.format(index, client[0], client[1]))

def handle_files(file_size, file_name):
    print('Recebendo arquivo')

    # Arquivos recebidos ficarão na pasta received_files
    if not os.path.isdir("received_files"):
        os.mkdir("received_files")

    data = bytearray()
    path = os.path.join("received_files", file_name)

    if os.path.isfile(path):
        os.remove(path)

    received = 0
    with open(path, 'ab+') as f:
        while received < file_size:
            if file_size - received >= 65536:
                packet = client_socket.recv(65536)
            else:
                packet = client_socket.recv(file_size - received)
            if not packet:
                return None
            
            pack_received = len(packet)
            received += pack_received
            data.extend(packet)
            f.write(data)
            data = bytearray()

    print('Arquivo: {} recebido\n'.format(file_name))
    show_commands()
    return

def send_files():
    try:
        print('Enviar arquivo')
        print('Coloque o diretório do arquivo que deseva enviar')
        
        file_path = input()
        selected_file = open(file_path, 'rb')

        file_name = os.path.basename(os.path.normpath(file_path))

        selected_file.seek(0, 2)
        file_size = selected_file.tell()
        selected_file.seek(0, 0)

        # Informações do arquivo que será enviado para os outros clientes
        pre_info = {'file_size': file_size, 'file_name': file_name}

        client_socket.send(pickle.dumps(pre_info))

        # Envia o arquivo selecionado
        sent = 0
        while True:
            if file_size - sent > 65536:
                buf = selected_file.read(65536)
            else:
                buf = selected_file.read(file_size - sent)

            if buf:
                client_socket.send(buf)
                sent += len(buf)
            else:
                break

        print('Arquivo enviado')
        return
    except IOError:
        print('Arquivo não encontrado')

def show_commands():
    print('\nAções:\n(1) - Enviar arquivo\n(2) - Listar clientes\n(3) - Sair\n')

def get_commands():
    global stop
    show_commands()
    command = input()

    if command == '3':
        print('Saindo...')
        client_socket.send(b"exit")
        client_socket.close()
        stop = True
    elif command == '2':
        update_screen()
    elif command == '1':
        send_files()
        get_commands()
    else:
        print('Comando inválido')
        get_commands()


response = client_socket.recv(2048)
response = pickle.loads(response)

clients = response['clients']

def clients_list():
    global clients
    while True:
        try:
            response = client_socket.recv(2048)
            response = pickle.loads(response)   

            if 'clients' in response:
                clients = response['clients']
                os.system('cls') or None
                show_clients()
                show_commands()
                
            if 'file_size' in response:
                handle_files(response['file_size'], response['file_name'])
            
            if stop:
                break

        except ConnectionAbortedError:
            client_socket.close()
            return


_thread.start_new_thread(clients_list, ())

update_screen()