from typing import Callable, Dict

import omu.client
from omu import Address, App, ConnectionListener, OmuClient
from omu.extension.table import Table, TableListener
from omuchat.event import EventHandler, EventKey, EventRegistry, events
from omuchat.model import Channel, Message, Provider, Room

from ..chat import ChatExtensionType


class _MessageListener(TableListener[Message]):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_add(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.event_registry.dispatch(events.MessageCreate, message)

    async def on_update(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.event_registry.dispatch(events.MessageUpdate, message)

    async def on_remove(self, items: Dict[str, Message]) -> None:
        for message in items.values():
            await self.event_registry.dispatch(events.MessageDelete, message)


class _ChannelListener(TableListener[Channel]):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_add(self, items: Dict[str, Channel]) -> None:
        for channel in items.values():
            await self.event_registry.dispatch(events.ChannelCreate, channel)

    async def on_update(self, items: Dict[str, Channel]) -> None:
        for channel in items.values():
            await self.event_registry.dispatch(events.ChannelUpdate, channel)

    async def on_remove(self, items: Dict[str, Channel]) -> None:
        for channel in items.values():
            await self.event_registry.dispatch(events.ChannelDelete, channel)


class _ProviderListener(TableListener[Provider]):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_add(self, items: Dict[str, Provider]) -> None:
        for provider in items.values():
            await self.event_registry.dispatch(events.ProviderCreate, provider)

    async def on_update(self, items: Dict[str, Provider]) -> None:
        for provider in items.values():
            await self.event_registry.dispatch(events.ProviderUpdate, provider)

    async def on_remove(self, items: Dict[str, Provider]) -> None:
        for provider in items.values():
            await self.event_registry.dispatch(events.ProviderDelete, provider)


class _RoomListener(TableListener[Room]):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_add(self, items: Dict[str, Room]) -> None:
        for room in items.values():
            await self.event_registry.dispatch(events.RoomCreate, room)

    async def on_update(self, items: Dict[str, Room]) -> None:
        for room in items.values():
            await self.event_registry.dispatch(events.RoomUpdate, room)

    async def on_remove(self, items: Dict[str, Room]) -> None:
        for room in items.values():
            await self.event_registry.dispatch(events.RoomDelete, room)


class _Listener(ConnectionListener):
    def __init__(self, registry: EventRegistry):
        self.event_registry = registry

    async def on_connected(self) -> None:
        await self.event_registry.dispatch(events.Ready)


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
        self.chat.channels.add_listener(_ChannelListener(self.event_registry))
        self.chat.providers.add_listener(_ProviderListener(self.event_registry))
        self.chat.rooms.add_listener(_RoomListener(self.event_registry))

    @property
    def loop(self):
        return self.omu.loop

    @property
    def messages(self) -> Table[Message]:
        return self.chat.messages

    @property
    def channels(self) -> Table[Channel]:
        return self.chat.channels

    @property
    def providers(self) -> Table[Provider]:
        return self.chat.providers

    @property
    def rooms(self) -> Table[Room]:
        return self.chat.rooms

    def run(self):
        self.omu.run()

    def on[**P](self, key: EventKey[P]) -> Callable[[EventHandler[P]], EventHandler[P]]:
        def decorator(func: EventHandler[P]) -> EventHandler[P]:
            self.event_registry.add(key, func)
            return func

        return decorator
