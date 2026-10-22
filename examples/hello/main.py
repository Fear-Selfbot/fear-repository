from fear_module import Command, FearModule
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message


class HelloModule(FearModule):
    name = "Hello"
    version = "1.0.0"
    author = "FUR Example"

    def register(self) -> None:
        command = Command("hello", ".", "Say hello")

        async def hello_handler(_client, message: Message) -> None:
            await message.edit("Hello from a FUR module!")

        command.add_handler(
            MessageHandler(hello_handler, command.filter & filters.me)
        )
        self.add_commands(command)
