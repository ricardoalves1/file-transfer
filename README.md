# File Transfer

FileTransfer é uma aplicação para tranferência de arquivos entre clientes, utilizando sockets (funções primitivas), desenvolvida em Python. 

O servidor utiliza threads para lidar com múltiplos clientes:
  
    _thread.start_new_thread(clients_list, ())

## Principais funcionalidades da aplicação

O Cliente pode:
- Adicionar arquivos para serem enviados a múltiplos clientes.
- Listar os clientes conectados;
- Desconectar-se do servidor.

# Dependências

## Python
Versão usada: 3.9

# Executando a aplicação
Utilizar Python3.

Para começar a executar a aplicação, primeiro deve-se iniciar o servidor e em seguida os clientes.

## 1º passo: Iniciar o servidor
Para iniciar o servidor, vá até o diretório do File Transfer e execute o seguinte comando:
```
  python3 server.py
```

## 2º passo: Iniciando os clientes
Abra outra aba no terminal, vá até o diretório do File Transfer e execute o seguinte comando:
```
  python3 client.py
```
(para uma completa experiência da aplicação, indicamos que repita o passo 2 mais duas vezes, para que tenha 3 clientes conectados na rede a fim de verificar as funcionalidades da aplicação)

## 3º passo: Escolher as ações do cliente
Ao se conectar, o cliente vê as seguintes opções:

    Ações:
    (1) - Enviar arquivo
    (2) - Listar clientes
    (3) - Sair

## Ações
### (1) - Enviar arquivo
Ao escolher a ação (1) será solicitado o seguinte ao cliente:

    Enviar arquivo
    Coloque o diretório do arquivo que deseva enviar

e o cliente deve colocar o caminho completo do arquivo, como:
     
     C:\Users\letic\Downloads\Instagram-Icone-3D (1).png
ao enviar o arquivo, o cliente receberá a mensagem de confirmação:

    Arquivo enviado

e imediatamento os demais clientes conectados irão receber o arquivo:

    Recebendo arquivo
    Arquivo: Instagram-Icone-3D (1).png recebido

e o servidor, por sua vez, também registra o recebimento do arquivo:

    Recebendo um arquivo
    sucesso em receber e salvar Instagram-Icone-3D (1).png para ('127.0.0.1', 50672)

e por fim, é possível ver todos os arquivos enviados pelos cliente na pasta **file-transfer\received_files**

    C:\LECodes\file-transfer\received_files [main ≡ +1 ~0 -0 !]> ls


        Diretório: C:\LECodes\file-transfer\received_files


    Mode                 LastWriteTime         Length Name
    ----                 -------------         ------ ----
    -a----        27/05/2021     16:02        1968661 Instagram-Icone-3D (1).png


### (2) - Listar clientes
Ao selecionar essa ação, será mostrado ao usuário a lista com todos os clientes conectados.

    Clientes conectados
    1 - 127.0.0.1:50538
    2 - 127.0.0.1:50672
    3 - 127.0.0.1:51079
    
E a cada conexão recebida, o servidor registrará da seguinte forma:

    Nova conexao recebida de ('127.0.0.1', 51079)
    {'clients': [('127.0.0.1', 50538), ('127.0.0.1', 50672), ('127.0.0.1', 51079)]}


### (3) - Sair
Na ação de Sair, o cliente será desconectado do servidor e o mesmo registrará a saída do cliente da seguinte forma:

    ('127.0.0.1', 51079) SUDDENLY DISCONNECTED
    {'clients': [('127.0.0.1', 50538), ('127.0.0.1', 50672)]}
