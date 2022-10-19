

# parsers and translates the raw messages from the network and commands the instrument controller

from network import *

@dataclass
class Commander:


    def __init__(self) -> bool:
        self.n = Network()
        self.n.initialize("192.168.8.70",5025, self.handle_socket_data)     # START THE NETWORK SOCKET MONITOR
        
        return
     
    def initialize(self, host:str, port:int ):
        return 

    def handle_socket_data(self,data:str):
        # this gets called back from Network
        print(f"From socket: {data}")
        return        


if __name__ == "__main__":

    import time
    print ("Main program ")
    


