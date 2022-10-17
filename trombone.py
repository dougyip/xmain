
import enum
from motor import *
from dataclasses import dataclass
import constants


@dataclass
class Trombone:

    def __init__(self,com_port_name : str) -> bool:

        #first serial port
        # GPIO14 for txc
        # GPIO15 FOR RXC
        # comportname == "/dev/ttyAMA0" # always the last digit is unique identifier for serial port
        # comportname == "/dev/ttyAMA1" # always the last digit is unique identifier for serial port
        
        self.com_port = serial.Serial(port = com_port_name, baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)
        self.com_port.isOpen()
        self.com_port.flushInput()
        self.com_port.flushOutput()
        self.com_port_name = com_port_name
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
        self.CalibrationTable = []
        # read the calibration table file for 5121 entries for Trombone
        if (self.read_cal_table == False):
            return False
        
     
    def initialize(self):
        # Initialize the Trombone ...
        # Read the calibration table into memory
        return 

    def set_CalibrationTable(self, index:int, value:int):
        self.CalibrationTable[index] = value

    def get_CalibrationTable(self, index:int):
        return self.CalibrationTable[index]

    def read_cal_table(self) -> bool:
        # fill the CalibrationTable with values from stored file or from NV_ file ? 
        filename = "ctstore" + self.com_port_name[-1] + ".txt"
        try:
            with open(filename,'r') as file:
                for eachline in file.readlines():
                    self.CalibrationTable.append(int((eachline).replace('\r',''))) 
        except FileNotFoundError:
            # The file was not found so create it
            print("file not found so creating cal_table_file")
            self.write_default_new_cal_table()
            self.read_cal_table()
            print(f"Cal Table # of items {len(self.CalibrationTable)}")
            if (len(self.CalibrationTable) == 5121):
                return True
            else:
                return False    # PROBLEM WITH CREATING CAL TABLE FILE
        return True
                    
    def write_default_new_cal_table(self):
        # filename of cal_table is based on the last char of the com_port_name to indicate different and unique trombones
        filename = 'ctstore' + self.com_port_name[-1] + ".txt"
        try:
            with open(filename,'w') as file:
                for index in range(0,5121):
                    file.write("0\r")
                file.close    
        except FileNotFoundError:
            # The file was not found so create it
            
            pass            

    def write_cal_table(self) -> bool:
        # write the contents of the entire cal_table to the file
        # filename of cal_table is based on the last char of the com_port_name to indicate different and unique trombones
        filename = 'ctstore' + self.com_port_name[-1] + ".txt"
        with open(filename,'w') as file:
            for index in range(0,5121):
                file.write(str(self.CalibrationTable[index]) + '\r')
            file.close
        return constants.ERR_NO_ERROR

    def set_Delay(self, value:int):
        # determine if ser or parallel mode
        # set the delay in the trombone only portion
        print (f"Set delay Trombone XT-100 {value}")
        return constants.ERR_NO_ERROR

    def set_delay(self, value : int, overshoot: bool, caltable: bool, callback: object  ) -> str:
        # THIS METHOD IS CALLED FROM THE DELAY OR SYSTEM CONTROLLER
        # value RANGE IS ALREADY CHECKED AND IS 0 >= value <= 625000 in units of fs
        print(f"set delay called with {value}") 
        
        # if overshoot is true move to overshoot position then move to final desired position

        _final_delay_setting = value
        _caltable_index = int((_final_delay_setting * 2)/1000)  # index into the caltable to get the offset amount
        _caltable_offset = self.CalibrationTable[_caltable_index]
        
        # NOTE: THE CALIBRATION TABLE ENTRY OFFSET IS IN FEMTOSECONDS UNITS, E.G. TABLE ENTRY OF -600 SHOULD BE == -0.60 ps
             
        if (overshoot == True):
            if (caltable == True):
                # move to overshoot position with caltable
                final_delay_pos_digital_steps = int((((_final_delay_setting - _caltable_offset)/1000) * constants.MOTOR_STEPS_PER_ONE_PS) + constants.MOTOR_STEPS_PER_FIVE_PS)
            else:
                # move to the overshoot position without caltable
                final_delay_pos_digital_steps = int(((_final_delay_setting/1000) * constants.MOTOR_STEPS_PER_ONE_PS) + constants.MOTOR_STEPS_PER_FIVE_PS)

            if (final_delay_pos_digital_steps > constants.MAX_NUMBER_MOTOR_STEPS):
                final_delay_pos_digital_steps = constants.MAX_NUMBER_MOTOR_STEPS
            elif (final_delay_pos_digital_steps < 0):
                final_delay_pos_digital_steps = 0
            
            print(f"digital step pos = {final_delay_pos_digital_steps}")
            
            self.Motor.set_delay_digital(final_delay_pos_digital_steps)
            # now set the current motor position to reflect the actual delay setting
            # TBD
            time.sleep(5.0)
           
        # move to final position
        if (caltable == True):
            # move to final position with caltable
            final_delay_pos_digital_steps = int(((_final_delay_setting - _caltable_offset)/1000) * constants.MOTOR_STEPS_PER_ONE_PS)
        else:
            # move to final position without caltable
            final_delay_pos_digital_steps = int((_final_delay_setting/1000) * constants.MOTOR_STEPS_PER_ONE_PS)

        if (final_delay_pos_digital_steps > constants.MAX_NUMBER_MOTOR_STEPS):
            final_delay_pos_digital_steps = constants.MAX_NUMBER_MOTOR_STEPS
        elif (final_delay_pos_digital_steps < 0):
            final_delay_pos_digital_steps = 0

        print(f"digital step pos = {final_delay_pos_digital_steps}")

        self.Motor.set_delay_digital(final_delay_pos_digital_steps)

        # now set the current motor position to reflect the actual delay setting


        return True
   
    def test_input_command(self):
        getinput = input()
        if ('DEL' in getinput):
            # DEL and value
            value = int(getinput[4:]) * 1000
            self.set_delay(value,True,True,None)
            pass
        else:
            motorcommand = getinput
            t.Motor.send_cmd(t.Motor.com_port,motorcommand,0.100)
            result = t.Motor.read_response(t.Motor.com_port)
            print (motorcommand, result)
    

if __name__ == "__main__":

    import time
    print ("Main program ")
    
    t = Trombone(constants.COM_PORT_5)

    # t.initialize()    # TTY/AMA0

    #t.write_cal_table()
    t.read_cal_table()
    
    inputvalue = input()
    
    t.set_delay(600000,True,True,None)

    while True:
        t.test_input_command()
#        t.test_input_command()
#        t.Motor.initialize()
    

