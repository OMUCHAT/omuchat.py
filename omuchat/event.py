from typing import Callable, Coroutine, Dict, List

from .model import Message


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

    def __call__(self, *args, **kwargs):
        return self.name


type EventHandler[T] = Callable[[T], Coroutine[None, None, None]]


class EventRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[EventKey, List[EventHandler]] = {}

    def add(self, key: EventKey, handler: EventHandler):
        if key not in self._handlers:
            self._handlers[key] = []
        self._handlers[key].append(handler)

    def remove(self, key: EventKey, handler: EventHandler):
        if key not in self._handlers:
            return
        self._handlers[key].remove(handler)

    async def dispatch[T](self, key: EventKey[T], data: T):
        if key not in self._handlers:
            return
        for handler in self._handlers[key]:
            await handler(data)


Ready = EventKey("ready")
MessageCreate = EventKey("on_message", Message)
MessageUpdate = EventKey("on_message_update", Message)
MessageDelete = EventKey("on_message_delete", Message)


class events:
    Ready = Ready
    MessageCreate = MessageCreate
    MessageUpdate = MessageUpdate
    MessageDelete = MessageDelete
    MessageDelete = MessageDelete
