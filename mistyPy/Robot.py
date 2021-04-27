from .RobotCommands import RobotCommands
from .Events import Event
from time import sleep
from requests import exceptions


class Robot(RobotCommands):
    def __init__(self, ip):
        self.__determine_ip(ip)
        self.active_event_registrations = {}

    def __determine_ip(self, ip: str):
        try:
            self.ip = "127.0.0.1"
            self.GetRequest("help")
        except exceptions.ConnectionError:
            self.ip = ip
            self.GetRequest("help")

    def RegisterEvent(self, event_name, event_type, condition=None, debounce=0, keep_alive=False, callback_function=None):
        if event_name is None or event_name == "":
            print(f"No event_name provided when registering to {event_type} - using default name {event_type}")
            event_name = event_type

        self.__remove_closed_events()

        if event_name in self.active_event_registrations:
            print(f"A registration already exists for event name {event_name}, ignoring request to register again")
            return

        new_registration = Event(self.ip, event_type, condition, debounce, keep_alive, callback_function)

        self.active_event_registrations[event_name] = new_registration

        return new_registration

    def UnregisterEvent(self, event_name):
        if not event_name in self.active_event_registrations:
            print(f"Not currently registered to event: {event_name}")
            return
        
        self.active_event_registrations[event_name].unsubscribe()
        del self.active_event_registrations[event_name]

    def UnregisterAllEvents(self):
        initial_event_names = list(self.active_event_registrations.keys())
        for event_name in initial_event_names:
            self.UnregisterEvent(event_name)

    def GetRegisteredEvents(self):
        self.__remove_closed_events()
        return self.active_event_registrations.keys()

    def KeepAlive(self):
        while True:
            sleep(1)

    def __remove_closed_events(self):
        events_to_remove = []

        for event_name, event_subscription in self.active_event_registrations.items():
            if not event_subscription.is_active:
                events_to_remove.append(event_name)

        for event_name in events_to_remove:
            print(f"Event connection has closed for event: {event_name}")
            self.UnregisterEvent(event_name)
