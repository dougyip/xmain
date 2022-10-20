

# parsers and translates the raw messages from the network and commands the instrument controller

from network import *

@dataclass
class Commander:


    def __init__(self) -> bool:
        self.n = Network()
        self.n.open_socket_and_listen("192.168.8.70",5025, self.handle_socket_data)     # START THE NETWORK SOCKET MONITOR
        
        return
     
    def initialize(self, host:str, port:int ):
        return 

    def handle_socket_data(self,data:str):
        # this gets called back from Network and contains the RAW socket data
        print(f"From socket: {data}")
        self.send_to_socket(data)
        return
    
    def send_to_socket(self,data:str):
        self.n.send_data_to_socket(data)        


if __name__ == "__main__":

    import time
    print ("Main program ")
    c = Commander()
        
    while True:
        pass

