from typing import Dict

from omu.client import Client, ClientListener
from omu.extension import Extension, define_extension_type
from omu.extension.endpoint.endpoint import ClientEndpointType, EndpointInfo
from omu.extension.server.model.extension_info import ExtensionInfo
from omu.extension.table import TableExtensionType
from omu.extension.table.model.table_info import TableInfo
from omu.extension.table.table import ModelTableType
from omu.interface import Serializer
from omuchat.model.author import Author, AuthorJson
from omuchat.model.channel import Channel, ChannelJson
from omuchat.model.message import Message, MessageJson
from omuchat.model.provider import Provider, ProviderJson
from omuchat.model.room import Room, RoomJson

ChatExtensionType = define_extension_type(
    ExtensionInfo.create("chat"), lambda client: ChatExtension(client), lambda: []
)


class ChatExtension(Extension, ClientListener):
    def __init__(self, client: Client) -> None:
        self.client = client
        client.add_listener(self)
        tables = client.extensions.get(TableExtensionType)
        self.messages = tables.register(MessagesTableKey)
        self.authors = tables.register(AuthorsTableKey)
        self.channels = tables.register(ChannelsTableKey)
        self.providers = tables.register(ProviderTableKey)
        self.rooms = tables.register(RoomTableKey)

    async def on_initialized(self) -> None:
        ...


MessagesTableKey = ModelTableType[Message, MessageJson](
    TableInfo.create(ChatExtensionType, "messages", use_database=True),
    Serializer.model(lambda data: Message.from_json(data)),
)
AuthorsTableKey = ModelTableType[Author, AuthorJson](
    TableInfo.create(ChatExtensionType, "authors"),
    Serializer.model(lambda data: Author.from_json(data)),
)
ChannelsTableKey = ModelTableType[Channel, ChannelJson](
    TableInfo.create(ChatExtensionType, "channels"),
    Serializer.model(lambda data: Channel.from_json(data)),
)
ProviderTableKey = ModelTableType[Provider, ProviderJson](
    TableInfo.create(ChatExtensionType, "providers"),
    Serializer.model(lambda data: Provider.from_json(data)),
)
RoomTableKey = ModelTableType[Room, RoomJson](
    TableInfo.create(ChatExtensionType, "rooms"),
    Serializer.model(lambda data: Room.from_json(data)),
)
FetchChannelsByUrlEndpoint = ClientEndpointType[str, Dict[str, Channel]](
    EndpointInfo.create(ChatExtensionType, "fetch_channels_by_url"),
    Serializer.noop(),
    Serializer.map(Serializer.model(Channel.from_json)),
)
