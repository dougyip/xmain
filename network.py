import enum
from dataclasses import dataclass
import constants
import socket
# from systemsettings import get_status,get_systemstatus

@dataclass
class Network:

    def __init__(self) -> bool:
        self.DATA = ""
        self.DATA_AVAILABLE_TO_SEND = False        
        return
        
    def handle_callback(self,data):
        print(f"got called back {data}")
        return       
    
    def send_data_to_socket(self,data):
        if (data != None):
            self.DATA = data.decode("UTF-8")
            self.DATA_AVAILABLE_TO_SEND = True
            return
        
    def initialize(self, host:str, port:int, callback):
        return 

    def open_socket_and_listen (self, host:str, port:int, callback):
        # HOST = "192.168.8.70"  # Standard loopback interface address (localhost)
        # PORT = 5025  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#            try:
            s.bind((host, port))
            s.listen()
            #s.setblocking(False)    # set this to False so it doesn't block
            conn, addr = s.accept()
            cumulative_data = ""
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    # TBD : SHOULD CHECK EACH CHARACTER FOR VALID ASCII
                    chars = data.decode("UTF-8")
                    if (chars == '\b'):
                        if ((len(cumulative_data) != 0) & (cumulative_data != None)):
                            # REMOVE LAST CHAR OF cumulative_data
                            cumulative_data = cumulative_data[:-1]
                    else:
                        if (chars != '\x7f'):  # ignore DEL key else add to cumulative_data
                            cumulative_data += str(chars)   
                    if ((chars == '\r') | (chars == '\n') | (chars == '\r\n')):
                        # \r or \n received
                        callback(str.encode(cumulative_data))
                        cumulative_data = ""
                    # ALSO IN THIS LOOP SEE IF THERE IS ANY DATA TO SEND
                    if (self.DATA_AVAILABLE_TO_SEND == True):
                        self.DATA_AVAILABLE_TO_SEND = False
                        # conn.send(str.encode(self.DATA))
            # except:
            #     print("Error socket and port already in use.")                      
            print("Connection to network was closed") 
        print("Connection to socket was closed")
        return 

        
if __name__ == "__main__":

    import time
    print ("Main program ")
    
    n = Network()
    
    n.open_socket_and_listen("192.168.8.70",5025,n.handle_callback)
    # SINCE .initialize STARTS A SOCKET AND CONNECTION, GETTING TO THIS POINT MEANS THAT THE SOCKET OR CONNECTION WAS CLOSED BY THE USER
    
    # RE-INITIALIZE AGAIN THE SOCKET CONNECTION
    n.open_socket_and_listen("192.168.8.70",5025,n.handle_callback)
    
    
