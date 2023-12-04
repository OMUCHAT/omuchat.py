from typing import Callable, Dict

import omu.client
from omu import Address, App, ConnectionListener, OmuClient
from omu.extension.table import TableListener

from omuchat.event import EventHandler, EventKey, EventRegistry, events
from omuchat.model import Message

from ..chat import ChatExtensionType


class _MessageListener(TableListener[Message]):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_add(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.event_registry.dispatch(EventKey("on_message"), message)

    async def on_update(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.event_registry.dispatch(EventKey("on_message_update"), message)

    async def on_remove(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.event_registry.dispatch(EventKey("on_message_delete"), message)


class _Listener(ConnectionListener):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_connected(self) -> None:
        await self.event_registry.dispatch(events.Ready, None)


class Client:
    def __init__(
        self,
        app: App,
        address: Address | None = None,
        client: omu.client.Client | None = None,
    ):
        self.app = app
        self.address = address or Address("127.0.0.1", 26423)
        self.omu = client or OmuClient(
            app=app,
            address=self.address,
        )
        self.event_registry = EventRegistry()
        self.chat = self.omu.extensions.register(ChatExtensionType)
        self.omu.connection.add_listener(_Listener(self.event_registry))
        self.chat.messages.add_listener(_MessageListener(self.event_registry))

    def run(self):
        self.omu.run()

    def on[T](self, key: EventKey[T]) -> Callable[[EventHandler[T]], EventHandler[T]]:
        def decorator(func: EventHandler[T]) -> EventHandler[T]:
            self.event_registry.add(key, func)
            return func

        return decorator
