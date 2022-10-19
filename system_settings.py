subscriptitons = dict()
system_settings = dict()

def subscribe(system_setting: str, fn):
    if not system_setting in subscriptitons:
        subscriptitons[system_setting] = []
    subscriptitons[system_setting].append(fn)

def post_event(system_setting: str, data):
    for fn in subscriptitons[system_setting]:
        fn(system_setting, data)

def set_status(key, value, index: int) -> None:
    if index is not None:
        system_settings[key][index] = value
    else:
        system_settings[key] = value
    if key in subscriptitons:
        post_event(key, value)

def get_status(key):
    return system_settings[key]

class Example_Watcher_1:
    def __init__(self):
        subscribe("network_active", self.handle_network_change_event)
        subscribe("network_ip", self.handle_network_change_event)
        subscribe("current_delay", self.handle_network_change_event)

    def handle_network_change_event(self, system_setting, data):
        print(f"W1: {system_setting} has changed to {data}")

class Example_Watcher_2:
    def __init__(self):
        subscribe("network_active", self.handle_network_change_event)
        subscribe("network_ip", self.handle_network_change_event)

    def handle_network_change_event(self, system_setting, data):
        print(f"W2: {system_setting} has changed to {data}")

def main():

    t1 = Example_Watcher_1()
    t2 = Example_Watcher_2()

    set_status("network_active", True, None)
    set_status("network_ip", ["192.168.8.20", "255.255.255.0", 2554], None)
    set_status("network_mac", "12:24:AB:CD:EF", None)
    set_status("network_conf", [True, "192.168.1.1", "Colby_1234"], None)
    set_status("network_ip", "255.255.0.0", 1)
    set_status("network_active", False, None)
    print(get_status("network_mac"))
    set_status("current_delay", 20000, None)

if __name__ == "__main__":
    main()

