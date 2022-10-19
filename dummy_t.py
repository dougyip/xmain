#Dummy trombone and relays for testing
import time
import pigpio

relay_module_addresses = {
    "ADDR_0": 0x20,
    "ADDR_1": 0x21,
    "ADDR_2": 0x22,
    "ADDR_3": 0x23,
    "ADDR_4": 0x24,
    "ADDR_5": 0x25,
    "ADDR_6": 0x26,
    "ADDR_7": 0x27
}


def set_trombone_delay(address, val, overshoot, use_cal_table, callback):
    print(f"Setting trombone {address} to {val:,}")
    time.sleep(.1)
    callback(1)
    return


INPUT_PORT = 0x00
OUTPUT_PORT = 0x01
POL_INV = 0x02
CONFIG = 0x03
BUS = 1

def set_relay_delay(i2c_address_map):

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


def main():
    sections = [[625000, "ADDR_0", 0], [1250000, "ADDR_0", 1], [2500000, "ADDR_1", 0], [5000000, "ADDR_1", 1], [10000000, "ADDR_2", 0], [20000000, "ADDR_2", 1],  [40000000, "ADDR_3", 1],  [80000000, "ADDR_3", 3]]
    out = init_relays(sections)
    print(out)

if __name__ == "__main__":
    main()
