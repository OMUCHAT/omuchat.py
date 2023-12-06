from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Coroutine, Dict, List

if TYPE_CHECKING:
    from .event import EventKey

type EventHandler[**P] = Callable[P, Coroutine[None, None, None]]


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

    async def dispatch[**P](self, key: EventKey[P], *args: P.args, **kwargs: P.kwargs):
        if key not in self._handlers:
            return
        for handler in self._handlers[key]:
            await handler(*args, **kwargs)
