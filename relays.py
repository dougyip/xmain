

class Relays:


    def __init__(self, model_type, _SystemSettings):

        # first arg = model type
        self.MODEL_TYPE = model_type

        # _SystemSettings instantiated when SystemController creates DelayProcessor
        # SystemSettings contains all the configuration information of instrument and NV parameters
        self.SystemSettings = _SystemSettings       # this makes SystemSettings accessible in this module
        return

    def calibration(self):
        # perform a self calibration on the relays
        return

    def initialize(self):
        # initialize all the relays
        return True

    def set_relay(self,RelayNumber,State):
        # set relay # to True(on) or False (off)

        print (f"set Relay #{RelayNumber+1} to {State}")
        return

    def get_relay(self,RelayNumber):
        # get the state of the current RelayNumber
        return





