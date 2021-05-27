import socket
import _thread
import pickle

# Clientes conectados
clients = []

def clients_list():
    list = []
    for client in clients:
        list.append(client[1])

    info = {'clients': list}

    print(info)
    for client in clients:
        client[0].sendto(pickle.dumps(info), client[1])

def search_server_input(tuple):
    for client in clients:
        if client[1] == tuple:
            return client[0]

    print("NO SERVER_INPUTS FOUND")
    return None

def server_handle_files(sock, file_size, file_name, sender):

    for client in clients:
        client = client[1]
        info = {'file_size': file_size, 'file_name': file_name}

        destination = (client[0], int(client[1]))
        if destination != sender:
            client_sock = search_server_input(destination) # pegar o socket
            if client_sock:
                client_sock.sendto(pickle.dumps(info), destination)

    # Pegar o arquivo enviado
    received = 0
    while received < file_size:
        if file_size - received >= 65536:
            packet = sock.recv(65536)
        else:
            packet = sock.recv(file_size - received)
        if not packet:
            return None

        pack_length = len(packet)

        received += pack_length

        for client in clients:
            client = client[1]
            destination = (client[0], int(client[1]))
            if destination != sender:
                client_sock = search_server_input(destination)
                if client_sock:
                    client_sock.sendto(packet, destination)
    
    print('sucesso em receber e salvar {} para {}'.format(file_name, server_input.getpeername()))
    return

def handle_response(server_input, addr, response):
    res = pickle.loads(response)

    # Verifica se será enviado algum arquivo 
    if 'file_size' in res:
        print("Recebendo um arquivo")

        server_handle_files(server_input, res['file_size'], res['file_name'], addr)
    else:
        print(res)

def on_new_client(server_input, addr):
    while True:
        try:
            response = server_input.recv(2048)

            if not response:
                print("NULL RESPONSE")
                clients.remove((server_input, addr))
                clients_list()
                break

            if response == b"exit":
                print(f'{addr} DISCONNECTED')
                clients.remove((server_input, addr))
                clients_list()
                break

            handle_response(server_input, addr, response)

        except ConnectionResetError:
            clients.remove((server_input, addr))
            print(f'{addr} SUDDENLY DISCONNECTED')
            clients_list()
            break

    server_input.close()
    return

address = ("localhost", 20000)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(address)
server_socket.listen(10)

print('Servidor iniciado')
print('Esperando clientes...')

while True:
    server_input, addr = server_socket.accept()
    print(f'Nova conexao recebida de {addr}')
    try:
        clients.append((server_input, addr))

        clients_list()

        _thread.start_new_thread(on_new_client, (server_input, addr))
    except ConnectionResetError:
        print(f'{addr} DID NOT LOGGED ON')