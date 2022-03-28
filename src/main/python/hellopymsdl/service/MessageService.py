import types
from importlib.resources import files


class MessageService:
    def __init__(self, resource_package: str | types.ModuleType = "hellopymsdl_rsrc"):
        self.__resource_package: str | types.ModuleType = resource_package  # pragma: no mutate

    def get_message(self, message_file_name: str) -> str:
        with files(self.__resource_package).joinpath(message_file_name).open() as file:
            return file.read()
