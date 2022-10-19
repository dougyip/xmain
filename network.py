import enum
from dataclasses import dataclass
import constants
import socket
# from systemsettings import get_status,get_systemstatus

@dataclass
class Network:

    def __init__(self) -> bool:
        
        return
        
        
    def initialize(self, host:str, port:int, callback:function):
        # HOST = "192.168.8.70"  # Standard loopback interface address (localhost)
        # PORT = 5025  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #    try:
            s.bind((host, port))
            s.listen()
        #    s.setblocking(False)    # set this to False so it doesn't block
            conn, addr = s.accept()
            cumulative_data = ""
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    cumulative_data += data.decode("UTF-8")
                    if (('\r' in cumulative_data) | ('\n' in cumulative_data)):
                        # \r received
                        callback(str.encode(cumulative_data))
                        cumulative_data = ""
                        
            return 


if __name__ == "__main__":

    import time
    print ("Main program ")
    
    n = Network()
    
    n.initialize("192.168.8.70",5025)
    