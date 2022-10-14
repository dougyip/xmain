import json
from dataclasses import dataclass
from abc import ABCMeta, abstractclassmethod, abstractmethod
import asyncio
import factory
import constants
import dummy_t

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
    _range = int
    _step = int
    __str__ = "RELAY"

    def initialize(self):            
        self._range = 2 * self.sections[-1][0]
        self._step = self.sections[0][0]
        print(f"   Initializiing Relay:")       
        print(f"   Relay has step of {self._step}")
        print(f"   Relay has range of {self._range}")
        print(f"   Relay has top_up {self.top_up}")

    def set_delay(self, val):
        if val > self._range:
            print(f"   Relay has top_up of {self.top_up[0]:,} turned on")
            val = val - self.top_up[0]
        print(f"   Relay delay is now {val:,}")

    def send_results(self, error_code):
        if self.error_code == 0:
            print(f"   Relay sucessfully set delay")
        else:
            print(f"   Relay failed to set delay")


@dataclass
class Channel(DelayComponent):
    channel_number: int
    size: int
    components: list
    _relay_index: int = None
    _trombone_index: int = None

    def initialize(self):
        print(f"Initializiing Channel {self.channel_number}")

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

        if val < self.size:
            t_val = 0
            # If this channel has both a relay and trombone
            if self._trombone_index is not None:
                if self.components[self._relay_index] is not None and val > self.components[self._relay_index]._range:
                    t_val = (val - self.components[self._relay_index].top_up[0]) % self.components[self._trombone_index].size           
                else:
                    t_val = val % self.components[self._trombone_index].size

                self.components[self._trombone_index].set_delay(t_val)
                val = val - t_val
            
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
            #print(f"Channel {channel.channel_number} of size {channel.size} has components {components}")

    for channel in channels: channel.initialize()
    channels[constants.CH1].set_delay(627000)
    channels[constants.CH2].set_delay(45000000)

if __name__ == "__main__":
    asyncio.run(main())