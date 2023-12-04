from omuchat.model.message import Message


class EventKey[T]:
    def __init__(self, name: str, type: type[T] | None = None):
        self.name = name
        self.type = type

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, EventKey):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


class events:
    Ready = EventKey("ready")
    MessageCreate = EventKey("on_message", Message)
    MessageUpdate = EventKey("on_message_update", Message)
    MessageDelete = EventKey("on_message_delete", Message)
