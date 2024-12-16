class EventDispatcher:
    def __init__(self):
        self.__listeners = {}

    def register(self, event_type, listener):
        if event_type not in self.__listeners:
            self.__listeners[event_type] = []
        self.__listeners[event_type].append(listener)

    def dispatch(self, event_type, *args, **kwargs):
        if event_type in self.__listeners:
            for listener in self.__listeners[event_type]:
                listener(*args, **kwargs)