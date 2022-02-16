"""MessageService tests"""

from unittest import TestCase

from hellopymsdl.service.MessageService import MessageService


class GetMessage(TestCase):
    """get_message method tests"""

    def test_resourceExists_should_returnMessage(self) -> None:
        """When resource exists, should return the resource message"""
        # GIVEN
        message_service: MessageService = MessageService("hellopymsdl_test_rsrc")

        # WHEN
        message: str = message_service.get_message("test_message.txt")

        # THEN
        self.assertEqual("A test message", message)

    def test_resourcePackageNotExists_should_raiseModuleNotFoundError(self) -> None:
        """When resource package doesn't exist, should raise a ModuleNotFoundError"""
        # GIVEN
        message_service: MessageService = MessageService("unknown_test_rsrc")

        # WHEN / THEN
        with self.assertRaises(ModuleNotFoundError):
            message_service.get_message("test_message.txt")

    def test_noneResourcePackage_should_raiseAttributeError(self) -> None:
        """When resource package is None, should raise an AttributeError"""
        # GIVEN
        # noinspection PyTypeChecker
        message_service: MessageService = MessageService(None)

        # WHEN / THEN
        with self.assertRaises(AttributeError):
            message_service.get_message("test_message.txt")

    def test_resourceNotExists_should_raiseFileNotFoundError(self) -> None:
        """When resource doesn't exist, should raise a FileNotFoundError"""
        # GIVEN
        message_service: MessageService = MessageService("hellopymsdl_test_rsrc")

        # WHEN / THEN
        with self.assertRaises(FileNotFoundError):
            message_service.get_message("unknown_message.txt")

    def test_noneResource_should_raiseTypeError(self) -> None:
        """When resource is None, should raise an TypeError"""
        # GIVEN
        # noinspection PyTypeChecker
        message_service: MessageService = MessageService("hellopymsdl_test_rsrc")

        # WHEN / THEN
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            message_service.get_message(None)
