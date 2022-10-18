import json
from dataclasses import dataclass
from abc import ABCMeta, abstractclassmethod, abstractmethod
import asyncio
import factory
import constants
import dummy_t
import pigpio

# Relay config.json indices (static constants) for code readibility
IDX_SIZE = 0
IDX_ADDR = 1
IDX_BITS = 2

class DelayComponent(metaclass=ABCMeta):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def set_delay(self, val):
        pass

@dataclass
class Trombone(DelayComponent):
    size: int
    address: int
    __str__ = "TROMBONE"

    def initialize(self):
        print(f"   Initializiing Trombone at address {self.address}")

    def set_delay(self, val):
        #print(f"Trombone at address {self.address} is now set to {val:,}")
        dummy_t.set_trombone_delay(self.address, val, True, True, self.send_results)

    def send_results(self, error_code):
        if error_code == 0:
            print(f"   Trombone at {self.address} sucessfully set delay")
        else:
            print(f"   Trombone at {self.address} failed to set delay")

@dataclass
class Relay(DelayComponent):
    sections: list
    top_up: list
    __str__ = "RELAY"

    def initialize(self):
        self._binary_sections_range = 2 * self.sections[-1][IDX_SIZE]
        self._step = self.sections[0][IDX_SIZE]
        print("   Initializiing Relay:")
        print(f"   Relay has step of {self._step}")
        print(f"   Relay has range of {self._binary_sections_range}")
        print(f"   Relay top_up is {self.top_up}")

        self._relay_modules = {}
        # Initialize _relay_modules dictionary with Relay section symbolic addresses
        for section in self.sections: 
            self._relay_modules[section[IDX_ADDR]] = 0
        if self.top_up is not None: self._relay_modules[self.top_up[IDX_ADDR]] = 0
        print(f"   Relay module i2c map is {self._relay_modules}")

        # Open i2c address handles
        BUS = 1
        pi = pigpio.pi()

        self._i2c_handles = []
        # Build list of i2c handles corresponding to the relay modules symbolic addresses
        for relay_module in self._relay_modules:
            #try:
                # handle = pi.i2c_open(BUS, dummy_t.relay_module_addresses[relay_module])
                # pi.i2c_write_byte_data(handle, dummy_t.CONFIG, 0)
                # self._i2c_handles.append(handle)
                
            self._i2c_handles.append(dummy_t.relay_module_addresses[relay_module])
            #except:
            #    print("Can't initialize i2c handles to Relay Modules")
            
        print(self._i2c_handles)


    def set_delay(self, val):
        print(f"Setting relays to {val}")
        # Check if the top_up Relay section needs to be activated
        if val >= self._binary_sections_range:
            self._relay_modules[self.top_up[IDX_ADDR]] |= self.top_up[IDX_BITS]
            print(f"   Relay has top_up of {self.top_up[IDX_SIZE]:,} turned on")
            val = val - self.top_up[IDX_SIZE]
        elif self.top_up is not None:
            self._i2c_address_map[self.top_up[IDX_ADDR]] &= ~(self.top_up[IDX_BITS])
        # Now determine which binary sections need to be activated
        val /= self._step
        bit_mask = 1
        for section in self.sections:
            print(f"   val = {int(val)} bit pointer = {bit_mask} list = {section}")
            if int(val) & bit_mask:
                self._relay_modules[section[IDX_ADDR]] |= section[IDX_BITS]
            else:
                self._relay_modules[section[IDX_ADDR]] &= ~(section[IDX_BITS])        
            bit_mask = bit_mask << 1

        print(f"   Generated 12c map {self._relay_modules}")
        print(f"   Binary relay sections are set to {int(self._step * val):,}")

        """ pi = pigpio.pi()
        OUTPUT_PORT = 0x01
        for idx, module in enumerate(self._relay_modules):
            pi.i2c_write_byte_data(self._i2c_handles[idx],  OUTPUT_PORT, module[IDX_BITS])
            # TODO Post update to delay progress value
            asyncio.time.sleep(0.20) """


    def send_results(self, error_code):
        if self.error_code == 0:
            print("   Relay sucessfully set delay")
        else:
            print("   Relay failed to set delay")


@dataclass
class Channel(DelayComponent):
    channel_number: int
    max_delay: int
    components: list

    def initialize(self):
        print(f"Initializiing Channel {self.channel_number}")
        self._relay_index: int = None
        self._trombone_index: int = None

        if any(obj.__str__ == 'RELAY' for obj in self.components):
            print(f"Channel {self.channel_number} has a Relay")
            self._relay_index = [obj.__str__ for obj in self.components].index('RELAY')
            print (f"Index of Relay is {self._relay_index}")
            self.components[self._relay_index].initialize()
        if any(obj.__str__ == 'TROMBONE' for obj in self.components):
            print(f"Channel {self.channel_number} has a Trombone")
            self._trombone_index = [obj.__str__ for obj in self.components].index('TROMBONE')
            print (f"Index of Trombone is {self._trombone_index}")
            self.components[self._trombone_index].initialize()

    def set_delay(self, val):
        self.delay = val
        #val = round()  #TODO Round the delay value down to the closest step size

        if val <= self.max_delay:
            # Determine delay value for Trombone if this channel has one
            if self._trombone_index is not None:
                # If the delay is the full range of the instrument then set trombone to its max
                if val == self.max_delay:
                    trombone_val = self.components[self._trombone_index].size
                # Else check if there's a relay top_up and factor that into the trombone delay calculation
                elif self.components[self._relay_index] is not None \
                    and val > self.components[self._relay_index]._binary_sections_range:
                    trombone_val = (val - self.components[self._relay_index].top_up[IDX_SIZE]) % self.components[self._trombone_index].size
                else:
                    trombone_val = val % self.components[self._trombone_index].size

                self.components[self._trombone_index].set_delay(trombone_val)
                # Subtract the Trombone's delay value 
                val -= trombone_val
            
            self.components[self._relay_index].set_delay(val)

            #TODO Need "success" responses from all the channel component set_delay() methods before updating the self.delay with val.


            print(f"Channel {self.channel_number} delay is now {self.delay:,}")

        else: 
            print("Desired delay value exceeds range of channel")
            #return ERROR_CODE

async def main() -> None:
    
    factory.register("trombone", Trombone)
    factory.register("relay", Relay)
    factory.register("channel", Channel)

    with open(constants.CONFIG_FILE) as file:
        data = json.load(file)

        # create the channels
        channels = [factory.create(item) for item in data["channels"]]
        # create the channel components
        for channel in channels:
            components = [factory.create(item) for item in channel.components]
            channel.components = components

    for channel in channels: channel.initialize()

    channels[constants.CH1].set_delay(199375000)
    channels[constants.CH2].set_delay(2500000)


if __name__ == "__main__":
    asyncio.run(main())
