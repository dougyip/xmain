import abc
from email.errors import ObsoleteHeaderDefect

class Subject:
    def __init__(self, subject):
        self._observers = set()
        self.subject = subject

    def subscribe(self, observer):
        self._observers.add(observer)

    def unsubscribe(self, observer):
        self._observers.discard(observer)

    def _notify_update(self, message):
        for observers in self._observers:
            observers.update([self.subject,message])


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, message):
        pass

class Microterminal(Observer):
    def update(self, message):
        print(f"Microterminal: Delay is now {message[1]}")

class WebUI(Observer):
    def update(self, message):
        print(f"WebUI: Delay is now {message[1]}")

class LCD(Observer):
    def update(self, message):
        if message[0] is "delay":
            print(f"LCD: Delay is now {message[1]}")

        elif message[0] is "network":
            print(f"LCD: Network address is now {message[1]}")

def main():
    delay_notifier = Subject("delay")
    network_notifier = Subject("network")

    mt = Microterminal()
    wui= WebUI()
    lcd = LCD()

    delay_notifier.subscribe(mt)
    delay_notifier.subscribe(wui)
    delay_notifier.subscribe(lcd)
    network_notifier.subscribe(mt)

    delay_notifier._notify_update("50ns")
    network_notifier._notify_update("192.168.1.1")
    delay_notifier._notify_update("10ns")
    delay_notifier._notify_update("200ns")
    network_notifier._notify_update("192.168.1.22")
    
if __name__ == "__main__":
    main()

