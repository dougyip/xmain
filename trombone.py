
import enum
from motor import *
from dataclasses import dataclass
import constants


@dataclass
class Trombone:

    def __init__(self,com_port_name) -> bool:

        #first serial port
        # GPIO14 for txc
        # GPIO15 FOR RXC
        # comportname == "/dev/ttyAMA0" # always the last digit is unique identifier for serial port
        # comportname == "/dev/ttyAMA1" # always the last digit is unique identifier for serial port
        
        self.com_port = serial.Serial(port = com_port_name, baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)
        self.com_port.isOpen()
        self.com_port.flushInput()
        self.com_port.flushOutput()

        # second serial port
        # GPIO4 TXD
        # GPIO5 RXDsc
        #self.com2 = serial.Serial(port = "/dev/ttyAMA1", baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)
        #self.com2.isOpen()
        #self.com2.flushInput()
        #self.com2.flushOutput()

        self.Motor = Motor(self.com_port)
        if (self.Motor.initialize() == False):
            # WHAT TO DO IF THERE IS A MOTOR INITIALIZATION PROBLEM HERE?
            print("MOTOR INITIALIZATION FAIL.")
            return False
        else:
            # NORMAL
            pass


        # READ THE CALIBRATION TABLE FILE
        self.CalibrationTable = [0,0]
        # read the calibration table file for 5120 entries for Primary Trombone
        
        
     
    def initialize(self):
        # Initialize the Trombone ...
        # Read the calibration table into memory

        return 


    def set_CalibrationTable(self,Index:int, Value:int):
        self.CalibrationTable[Index] = Value

    def get_CalibrationTable(self,Index:int):
        return self.CalibrationTable[Index]

    def read_CalibrationTable_from_file(self):
        # fill the CalibrationTable with values from stored file or from NV_ file ? 
        
        try:
            with open('ctstore0.txt','r') as file:
                for eachline in  file.readlines():
                    self.CalibrationTable.append(int((eachline).replace('\r','')))             
        except FileNotFoundError:
            # The file was not found so create it
            
            pass            
    def write_CalibrationTable_to_file(self):
        # fill the CalibrationTable with values from stored file or from NV_ file ? 
        
        try:
            with open('ctstore0.txt','w') as file:
                for index in range(0,5120):
                    file.writeline('0')
                file.close    
        except FileNotFoundError:
            # The file was not found so create it
            
            pass            


    def set_Delay(self,Value:int):
        # determine if ser or parallel mode
        # set the delay in the trombone only portion
        print (f"Set delay Trombone XT-100 {Value}")
        
        
        
        
        
        
        
        return constants.ERR_NO_ERROR

    def set_delay(value : int, overshoot: bool, caltable: bool, callback: object  ) -> str:
        # python
        # set the delay to value in fs
        print(f"setting delay to {value}")     
        
        
        

                    
    
    def set_Delay_Primary(self,Value):
        print (f"Set delay CH1 XT-200 {Value}")
        return constants.ERR_NO_ERROR

    def set_Delay_Secondary(self,Value):
        print (f"Set delay CH2 XT-200 {Value}")
        return constants.ERR_NO_ERROR
    
    def test_input_command(self):
        getinput = input()
        motorcommand = getinput
        t.Motor.send_cmd(t.Motor.com1,motorcommand,0.100)
        result = t.Motor.read_response(t.Motor.com1)
        print (motorcommand, result)
    

if __name__ == "__main__":

    import time
    print ("Main program ")
    
    t = Trombone(constants.COM_PORT_5)

    # t.initialize()    # TTY/AMA0

    t.write_CalibrationTable_to_file
    t.read_CalibrationTable_from_file()



    while True:
        t.test_input_command()
        t.test_input_command()
        t.Motor.initialize()
    

