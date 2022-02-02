import types
from importlib.resources import files


class MessageService:
    def __init__(self, message_file_name: str, resource_package: str | types.ModuleType = "hellopysdl_rscr"):
        self.__resource_package: str = resource_package
        self.__message_file_name: str = message_file_name

    def get_message(self) -> str:
        with files(self.__resource_package).joinpath(self.__message_file_name).open() as file:
            return file.read()
