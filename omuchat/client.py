from typing import Callable, Dict

import omu.client
from omu import Address, App, ConnectionListener, OmuClient
from omu.extension.table import TableListener

from omuchat.event import EventHandler, EventKey, EventRegistry

from .chat import ChatExtensionType
from .event import events
from .model import Message


class MessageListener(TableListener[Message]):
    def __init__(self, handlers: EventRegistry):
        self.handlers = handlers

    async def on_add(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.handlers.dispatch(EventKey("on_message"), message)

    async def on_update(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.handlers.dispatch(EventKey("on_message_update"), message)

    async def on_remove(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.handlers.dispatch(EventKey("on_message_delete"), message)


class Listener(ConnectionListener):
    def __init__(self, handlers: EventRegistry):
        self.handlers = handlers

    async def on_connected(self) -> None:
        await self.handlers.dispatch(events.Ready, None)


class Client:
    def __init__(
        self,
        app: App,
        address: Address | None = None,
        client: omu.client.Client | None = None,
    ):
        self.app = app
        self.omu = client or OmuClient(
            app=app,
            address=address or Address("127.0.0.1", 26423),
        )
        self.chat = self.omu.extensions.register(ChatExtensionType)
        self.event_handlers = EventRegistry()
        self.omu.connection.add_listener(Listener(self.event_handlers))
        self.chat.messages.add_listener(MessageListener(self.event_handlers))

    def run(self):
        self.omu.run()

    def on[T](self, key: EventKey[T]) -> Callable[[EventHandler[T]], EventHandler[T]]:
        def decorator(func: EventHandler[T]) -> EventHandler[T]:
            self.event_handlers.add(key, func)
            return func

        return decorator
