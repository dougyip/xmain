
import pigpio
import time

# DONE IN CONFIG.TXT dtparam=i2c_arm=on
# THIS DOES NOT USE SPI TO CONTROL THE BARGRAPH
# 

# RELAY SECTION ADDRESSES
SECTION_0_ADDR = 0x20
SECTION_1_ADDR = 0x21
SECTION_2_ADDR = 0x22
SECTION_3_ADDR = 0x23
SECTION_4_ADDR = 0x24
SECTION_5_ADDR = 0x25
SECTION_6_ADDR = 0x26
SECTION_7_ADDR = 0x27

# GPIO2 is SDA
# GPIO3 is SCL

INPUT_PORT = 0x00
OUTPUT_PORT = 0x01
POL_INV = 0x02
CONFIG = 0x03
ZEROES = 0x00
ALL_ONES = 0xFF
RELAY_ONE = 0x01
RELAY_TWO = 0x02
RELAY_BOTH = 0x03

BUS = 1

if __name__ == "__main__":


    HW = pigpio.pi()

    # print (HW.get_pigpio_version)
    # HW.set_mode(2, pigpio.ALT0)   # DONE IN CONFIG.TXT dtparam=i2c_arm=on
    # HW.set_mode(3, pigpio.ALT0)   # 

    # EACH OF THE SECTION ADDRESSES HAVE BEEN TESTED FOR OPEN AND WRITE BYTE DATA
    # ERROR IF HW RELAY SECTION ADDRESS AND RELAY BOARD ARE NOT INSTALLED

    handle = HW.i2c_open(BUS, SECTION_0_ADDR)   # ONLY OPEN THE SECTION IF CONNECTED

    try:
        HW.i2c_write_byte_data(handle, CONFIG, ZEROES)   # TO SET AS OUTPUT
        # DO NOT WRITE BYTE DATA TO RELAY SECTIONS THAT ARE NOT CONNECTED ONTO THE BUS

    except:
        print("i2c_write_byte_data")

    while True:

        #    char _RelayPairAddrStateSetting; // 0b000000XY, X=Relay_Two ON/OFF, Y=Relay_One ON/OFF
        # WRITE_BYTE_DATA WILL FAIL IF RELAY IS NOT CONNECTED AND ADDRESSED CORRECTLY
        # ADD TRY: EXCEPT: TO CATCH THE FAIL CONDITION
        # TBD
        HW.i2c_write_byte_data(handle, OUTPUT_PORT, ZEROES) # OFF
        time.sleep(0.100)

        HW.i2c_write_byte_data(handle, OUTPUT_PORT, RELAY_ONE)   # REL 1 ON
        time.sleep(0.100)

        HW.i2c_write_byte_data(handle, OUTPUT_PORT, RELAY_TWO)   # REL 2 ON
        time.sleep(0.100)

        HW.i2c_write_byte_data(handle, OUTPUT_PORT, RELAY_BOTH)   # ALL ON    
        time.sleep(0.100)

        HW.i2c_write_byte_data(handle, OUTPUT_PORT, ZEROES)   # ALL OFF
        time.sleep(0.100)

