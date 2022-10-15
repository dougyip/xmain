
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
        # read the calibration table file for 5121 entries for Primary Trombone
        if (self.read_cal_table == False):
            return False
        
     
    def initialize(self):
        # Initialize the Trombone ...
        # Read the calibration table into memory
        return 


    def set_CalibrationTable(self,Index:int, Value:int):
        self.CalibrationTable[Index] = Value

    def get_CalibrationTable(self,Index:int):
        return self.CalibrationTable[Index]

    def read_cal_table(self):
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


    def set_Delay(self,Value:int):
        # determine if ser or parallel mode
        # set the delay in the trombone only portion
        print (f"Set delay Trombone XT-100 {Value}")
        return constants.ERR_NO_ERROR

    def set_delay(value : int, overshoot: bool, caltable: bool, callback: object  ) -> str:
        # 
        # set the delay to value in fs, value is >=0 and value <= 625000 fs
        print(f"setting delay to {value}") 
        
        # delay value must be >=0 and <= 625.0
        # if overshoot is true move to overshoot position then move to final desired position

        _final_delay_setting = value
        _delay_setting_with_ovs = value + 5000
        _caltable_index = int((_final_delay_setting * 2)/1000)  # index into the caltable to get the offset amount
        #// NOTE: THE CALIBRATION TABLE ENTRY OFFSET IS IN FEMTOSECONDS UNITS, E.G. TABLE ENTRY OF -600 SHOULD BE == -0.60 ps
 
                
        if (overshoot == True):
            # move to overshoot position
            final_delay_pos_digital = 
            _TEMP_f = ((_FinalCP_DelaySetting_PS - _CalTableEntryOffsetAmount) * MOTOR_STEPS_PER_ONE_PS) + MOTOR_STEPS_PER_FIVE_PS;
                    _MotorPositionDIGITAL = (long)_TEMP_f;

                    if (_MotorPositionDIGITAL > MAX_NUMBER_MOTOR_STEPS) // Final Calibrated Position + 8325 STEPS is beyond limit, then adjust amount
                    {
                        _MotorPositionDIGITAL = MAX_NUMBER_MOTOR_STEPS;
                    }
                    // 07.21.21 IF CALC POSITION IS NEG, MAKE IT ZERO
                    if (_MotorPositionDIGITAL < 0)
                        _MotorPositionDIGITAL = 0;
                    MOTOR_SetDelayDigital(_MotorPositionDIGITAL);
                    MOTOR.CurrentDelaySettingPS = _DelaySetting_PS + (MOTOR_STEPS_PER_FIVE_PS / MOTOR_STEPS_PER_ONE_PS); // use a min of fix to reflect DESIRED delay setting
                                                                                                                         // printf("OVERSHOOT _MotorPositionDIGITAL, Fcp, Fcp offset = %lu, %6.2f, %6.2f \n", _MotorPositionDIGITAL, _FinalCP_DelaySetting_PS, _CalTableEntryOffsetAmount);

            
            
            pass
            
        # move to final position
        if (caltable == True):
            # use caltable to compute final position
            pass
        else:
            # compute final position without caltable use
            pass
                                
        
            """
            if ((((_DelaySetting_FS >= 0) && (_DelaySetting_FS < 625000))) ||
            ((_DelaySetting_FS == 625000) && (((strcmp(INSTRUMENT.deviceOPTION, "000") == 0) ||
                                               (strcmp(INSTRUMENT.deviceOPTION, "OEM") == 0) ||
                                               (INSTRUMENT.stateDEVICE_MODE == DEVICE_PARALLEL)))))
            {
            if ((g_NVParameters.nv_overshoot == TRUE) && (MOTOR.CurrentDelaySettingPS < _DelaySetting_PS))
            {
                // MOVE TO OVERSHOOT POSITION THEN MOVE TO THE FINAL DESIRED POSITION

                _FinalCP_DelaySetting_PS = _DelaySetting_PS;
                _DelaySettingPS_With_Overshoot = _DelaySetting_PS + _OvershootAmount;

                if (GLOBAL_SETTINGS.USE_CAL_TABLE == TRUE)
                {
                    // 04.30.18 // use a calibrated correction position
                    // 04.30.18 // determine the index to get the calibration offset
                    // 04.30.18 // if SIZE_CAL_TABLE == 1251 then calibration offsets are at 0.500 ps steps
                    // 04.30.18 // if SIZE_CAL_TABLE == 6251 then calibration offsets are at 0.100 ps steps

                    if (SIZE_CAL_TABLE == 1251)
                    {
                        // multiply _DelaySetting_PS by 10 (since calibration table fixes are at each 100 fs)
                        _CalTableDesiredDelayIndex = (int)(_FinalCP_DelaySetting_PS * 2);
                    }
                    else
                    {
                        _CalTableDesiredDelayIndex = 0;
                    }

                    // 02.03.21 IF THE INDEX IS ABOVE 1250 THEN USE 0 AS THE OFFSET
                    if (_CalTableDesiredDelayIndex <= 1250)
                    {
                        #// NOTE: THE CALIBRATION TABLE ENTRY OFFSET IS IN FEMTOSECONDS UNITS, E.G. TABLE ENTRY OF -600 SHOULD BE == -0.60 ps
                        // THEREFORE DIVIDE BY 1000.0 TO GET PS UNITS
                        _CalTableEntryOffsetAmount = (float)(g_NVParameters.nv_cal_table[_CalTableDesiredDelayIndex] / 1000.0);
                    }
                    else
                    {
                        _CalTableEntryOffsetAmount = 0;
                    }

                    // COMPUTE THE NEW DESIRED POSITION IN DIGITAL INT
                    //_MotorPositionDIGITAL = (unsigned long)((_FinalCP_DelaySetting_PS - _CalTableEntryOffsetAmount) * MOTOR_STEPS_PER_ONE_PS) + MOTOR_STEPS_PER_FIVE_PS;
                    _TEMP_f = ((_FinalCP_DelaySetting_PS - _CalTableEntryOffsetAmount) * MOTOR_STEPS_PER_ONE_PS) + MOTOR_STEPS_PER_FIVE_PS;
                    _MotorPositionDIGITAL = (long)_TEMP_f;

                    if (_MotorPositionDIGITAL > MAX_NUMBER_MOTOR_STEPS) // Final Calibrated Position + 8325 STEPS is beyond limit, then adjust amount
                    {
                        _MotorPositionDIGITAL = MAX_NUMBER_MOTOR_STEPS;
                    }
                    // 07.21.21 IF CALC POSITION IS NEG, MAKE IT ZERO
                    if (_MotorPositionDIGITAL < 0)
                        _MotorPositionDIGITAL = 0;
                    MOTOR_SetDelayDigital(_MotorPositionDIGITAL);
                    MOTOR.CurrentDelaySettingPS = _DelaySetting_PS + (MOTOR_STEPS_PER_FIVE_PS / MOTOR_STEPS_PER_ONE_PS); // use a min of fix to reflect DESIRED delay setting
                                                                                                                         // printf("OVERSHOOT _MotorPositionDIGITAL, Fcp, Fcp offset = %lu, %6.2f, %6.2f \n", _MotorPositionDIGITAL, _FinalCP_DelaySetting_PS, _CalTableEntryOffsetAmount);
                }
                else
                {
                    // MOTOR_SetDelay(_DelaySetting_PS + _OvershootAmount); // add overshoot amount only (CAL TABLE NOT USED)
                    // COMPUTE THE NEW DESIRED POSITION IN DIGITAL INT
                    _MotorPositionDIGITAL = (long)(_DelaySettingPS_With_Overshoot * MOTOR_STEPS_PER_ONE_PS);
                    // 07.21.21 IF CALC POSITION IS NEG, MAKE IT ZERO
                    if (_MotorPositionDIGITAL < 0)
                        _MotorPositionDIGITAL = 0;
                    MOTOR_SetDelayDigital(_MotorPositionDIGITAL);

                    // if using the CAL TABLE, then INSTRUMENT_SETTINGS.CurrentDelay AND MOTOR.CurrentDelaySettingPS
                    // SHOULD be the _DelaySetting_PS value rather than the ACTUAL included CALIBRATION OFFSET amount
                    MOTOR.CurrentDelaySettingPS = _DelaySetting_PS;       // fix to reflect DESIRED delay setting
                    INSTRUMENT_SETTINGS.CURRENT_DELAY = _DelaySetting_PS; // 02.07.08
                }
            } // end-if

            // MOVE TO FINAL POSITION (AND CHECK FOR CALIBRATION TABLE ON/OFF)
            if (GLOBAL_SETTINGS.USE_CAL_TABLE == TRUE)
            {
                // 04.30.18 // USE A CALIBRATED CORRECTION POSITION
                // 04.30.18 // DETERMINE THE INDEX TO GET THE CALIBRATION OFFSET
                // 04.30.18 // if SIZE_CAL_TABLE == 1251 then calibration offsets are at 0.500 ps steps
                // 04.30.18 // if SIZE_CAL_TABLE == 6251 then calibration offsets are at 0.100 ps steps
                if (SIZE_CAL_TABLE == 1251)
                {
                    _CalTableDesiredDelayIndex = (int)(_DelaySetting_PS * 2);
                }
                else
                {
                    _CalTableDesiredDelayIndex = 0;
                }

                _CalTableEntryOffsetAmount = (float)(g_NVParameters.nv_cal_table[_CalTableDesiredDelayIndex] / 1000.0);

                // MOTOR_SetDelay(_DelaySetting_PS - _CalTableEntryOffsetAmount );  // should be MINUS the Offset Amount (not PLUS) 02.03.18
                INSTRUMENT.stateMOTOR_MOVE_CHECK_OPC = TRUE; // SIGNAL THAT THIS IS THE LAST MOVEMENT
                // COMPUTE THE NEW DESIRED POSITION IN DIGITAL INT
                _MotorPositionDIGITAL = (long)((_DelaySetting_PS - _CalTableEntryOffsetAmount) * MOTOR_STEPS_PER_ONE_PS);
                // 07.21.21 IF CALC POSITION IS NEG, MAKE IT ZERO
                if (_MotorPositionDIGITAL < 0)
                    _MotorPositionDIGITAL = 0;
                MOTOR_SetDelayDigital(_MotorPositionDIGITAL);
                // printf("FINAL _MotorPositionDIGITAL, Fcp, offset  = %lu , %6.2f, %6.2f \n", _MotorPositionDIGITAL, _DelaySetting_PS, _CalTableEntryOffsetAmount);

                // if using the CAL TABLE, then INSTRUMENT_SETTINGS.CurrentDelay AND MOTOR.CurrentDelaySettingPS
                // SHOULD be the _DelaySetting_PS value rather than the ACTUAL included CALIBRATION OFFSET amount
                MOTOR.CurrentDelaySettingPS = _DelaySetting_PS;       // fix to reflect DESIRED delay setting
                INSTRUMENT_SETTINGS.CURRENT_DELAY = _DelaySetting_PS; // 02.07.08
            }
            else
            {
                // MOTOR_SetDelay(_DelaySetting_PS);
                INSTRUMENT.stateMOTOR_MOVE_CHECK_OPC = TRUE; // SIGNAL THAT THIS IS THE LAST MOVEMENT
                // COMPUTE THE NEW DESIRED POSITION IN DIGITAL INT
                _MotorPositionDIGITAL = (long)(_DelaySetting_PS * MOTOR_STEPS_PER_ONE_PS);
                // 07.21.21 IF CALC POSITION IS NEG, MAKE IT ZERO
                if (_MotorPositionDIGITAL < 0)
                    _MotorPositionDIGITAL = 0;
                MOTOR_SetDelayDigital(_MotorPositionDIGITAL);

                // if using the CAL TABLE, then INSTRUMENT_SETTINGS.CurrentDelay AND MOTOR.CurrentDelaySettingPS
                // SHOULD be the _DelaySetting_PS value rather than the ACTUAL included CALIBRATION OFFSET amount
                MOTOR.CurrentDelaySettingPS = _DelaySetting_PS;       // fix to reflect DESIRED delay setting
                INSTRUMENT_SETTINGS.CURRENT_DELAY = _DelaySetting_PS; // 02.07.08
            }

            if (INSTRUMENT.stateDEVICE_MODE == DEVICE_SERIAL)
            {
                HWIO_REL_SetRelays_X_SER(0x0000); // TURN OFF ALL THE RELAYS
                for (_j = 1; _j <= HW_RELAYS.NUM_OF_SECTIONS; _j++)
                {
                    HW_RELAYS.RELAY_ON_OFF[_j] = OFF;
                } // end-for
            }     // end-if

        } // bad 06-16-21}		  // end-if

        """    
        return True
   
    def test_input_command(self):
        getinput = input()
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

    while True:
        t.test_input_command()
        t.test_input_command()
        t.Motor.initialize()
    

