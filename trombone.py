
import enum
from motor import *
from dataclasses import dataclass

# SystemController CLASS
ERR_NO_ERROR = -1
ERR_INVALID_ARG = 1
ERR_NO_CALIBRATION = 2
ERR_DELAY_NOT_SET = 3
ERR_DELAY_OUT_OF_RANGE = 4

COM_PORT_5 = "/dev/ttyAMA0"
COM_PORT_3 = "/dev/ttyAMA1"

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
        



        self.CalibrationTable_PRI = [0,0]
        self.CalibrationTable_SEC = [0,0]
        
        # read the calibration table file for 5120 entries for Primary Trombone
        # read the calibration table file for 5120 entries for Secondary Trombone
        
        
     
    def initialize(self):
        # Initialize the Trombone ...
        # Read the calibration table into memory

        return 


    def set_CalibrationTable(self,Index,Value):
        self.CalibrationTable[Index] = Value

    def get_CalibrationTable(self,Index):
        return self.CalibrationTable[Index]

    def read_CalibrationTable_from_file(self):
        # fill the CalibrationTable with values from stored file or from NV_ file ? 
        pass

    def set_Delay(self,Value):
        # determine if ser or parallel mode
        # set the delay in the trombone only portion
        print (f"Set delay Trombone XT-100 {Value}")
        return ERR_NO_ERROR

    def set_delay(self, pri_sec:enum, value : int, overshoot: bool, caltable: bool, callback: object  ) -> None:
        if (pri_sec == 'PRI'):
            # determine which COM port to use whether XT-100 or XT-200 PRIMARY
            pass
        else:
            # use the com port for secondary trombone XT-200 SECONDARY
            pass

                    
    
    def set_Delay_Primary(self,Value):
        print (f"Set delay CH1 XT-200 {Value}")
        return ERR_NO_ERROR

    def set_Delay_Secondary(self,Value):
        print (f"Set delay CH2 XT-200 {Value}")
        return ERR_NO_ERROR
    
    def test_input_command(self):
        getinput = input()
        motorcommand = getinput
        t.Motor.send_cmd(t.Motor.com1,motorcommand,0.100)
        result = t.Motor.read_response(t.Motor.com1)
        print (motorcommand, result)


        

    

if __name__ == "__main__":

    import time
    print ("Main program ")
    
    t = Trombone()

    t.initialize(COM_PORT_5)    # TTY/AMA0


    while True:
        t.test_input_command()
        t.test_input_command()
        t.Motor.initialize()
    

