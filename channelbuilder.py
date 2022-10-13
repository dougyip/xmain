import json
from dataclasses import dataclass
from abc import ABCMeta, abstractclassmethod, abstractmethod
from pickle import FALSE

from numpy import array, empty

import factory
import constants

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
    __str__: str = "TROMBONE"

    def initialize(self):
        print(f"Initializiing Trombone at address {self.address}")

    def set_delay(self, val):
        print(f"Trombone at address {self.address} is now set to {val:,}")

    def send_results(self, error_code):
        if self.error_code == 0:
            print(f"Trombone at {self.address} sucessfully set delay")
        else:
            print(f"Trombone at {self.address} failed to set delay")

@dataclass
class Relay(DelayComponent):
    size: int
    step: int
    sections: list
    top_up: list
    __str__: str = "RELAY"

    def initialize(self):
        print(f"Initializiing Relay")

    def set_delay(self, val):
        print(f"Relay delay is now {val:,}")

    def send_results(self, error_code):
        if self.error_code == 0:
            print(f"Relay sucessfully set delay")
        else:
            print(f"Relay failed to set delay")


    def list_sections(self):
        print(f"Relay section map {self.sections}")

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
            #If val > maximum range of binary relay sections, subtract the size of the top_up section from the 'val' and activate that i2c address.
            if self._relay_index is not None and val > self.components[self._relay_index].size:
                #turn on top_up section
                val = val - self.components[self._relay_index].top_up[0]
                print(f"Relay on channel {self.channel_number} has top_up turned on")
            if self._trombone_index is not None:
                tval = val % self.components[self._trombone_index].size
                self.components[self._trombone_index].set_delay(tval)
                val = val - tval
            if self._relay_index is not None:
                self.components[self._relay_index].set_delay(val)


            #TODO Need "success" responses from all the channel component set_delay() methods before updating the self.delay with val.


            print(f"Channel delay is now {self.delay:,}")

        else: 
            print("Desired delay value exceeds range of channel")
            #return ERROR_CODE

def main() -> None:
    
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
    channels[constants.CH2].set_delay(120000)

if __name__ == "__main__":
    main()