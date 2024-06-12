from enum import Enum
from socket import socket
from typing import Dict
class Estado(Enum):
    DONE = 1
    PENDING = 2
    FREE = 3

class ChunkFile:
    first:int =0
    last:int=0
    estado:Estado=Estado.FREE
    def __init__(self,first:int=0,last:int=0,estado:Estado=Estado.FREE):
        self.first=first
        self.last=last
        self.estado=estado
    def ultimo(self,last:int):
        self.last=last
    def primer(self,primer:int):
        self.first=primer
    def __str__(self):
        return f"{self.first}-{self.last}"
    
class FileReader:
    wordlist:str=""
    file_size:int=0

    chunk_list:list[ChunkFile]=[]
    pending_chunk:list[ChunkFile]=[]
    done_chunks:list[ChunkFile]=[]
    
    number_of_chunks:int=0
    chunk_size:int = 0
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(FileReader, cls).__new__(cls)
    #     return cls.instance
    def __init__(self, wordlist:str="rockyou",number_of_chunks:int=10,file_size:int=139921497):
        # need total size
        self.chunk_list=[]
        self.pending_chunk=[]
        self.done_chunks=[]
        
        self.wordlist=wordlist
        self.file_size=file_size
        self.number_of_chunks=number_of_chunks
        self.chunk_size = file_size // number_of_chunks

        for i in range(number_of_chunks): #n=4
            start = i * self.chunk_size if i == 0 else (i * self.chunk_size)-15 #no hay linea mayor de 15 bytes; así aseguramos que no se parten lineas
            if i == number_of_chunks - 1:
                end = file_size  # Ensure the last segment goes up to the end
            else:
                end = i * self.chunk_size + self.chunk_size
            self.chunk_list.append(ChunkFile(first=start,last=end))

        # if self.wordlist != wordlist:
        #     self.wordlist = wordlist
        #     self.chunk_size=chunk_size
        #     self.last_requests = {socket:ChunkFile}
        #     self._fill_chunks()
        # else:
        #     for i in self.chunk_list:
        #         i.estado=Estado.FREE
    
    def assign_chunk(self, requested_by:socket)->ChunkFile: 
        tmp_chunk = self.chunk_list.pop(0)
        tmp_chunk.estado=Estado.PENDING
        self.pending_chunk.append(tmp_chunk)
        #self.last_requests[requested_by] = tmp_chunk
        return tmp_chunk

    def hasFree(self)->bool:
        return len(self.chunk_list)!=0
    def stats(self):
        print(f"TODO: {len(self.chunk_list)}")
        for i in self.chunk_list:
            print(i)
        print("Pending: ",len(self.pending_chunk),"\nDone: ",len(self.done_chunks))
        
    # def check_request(self, resquested_by:socket)->bool:
    #     if resquested_by in self.last_requests and self.last_requests[resquested_by] is not None:
    #         return True
    #     return False
    """True if all packages sended and received"""
    
    

