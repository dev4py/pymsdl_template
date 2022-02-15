from unittest import TestCase

from hellopymsdl.service.MessageService import MessageService


class MessageServiceTest(TestCase):
    def test_get_message(self) -> None:
        """
        a doc
        :return:
        """
        # GIVEN
        message_service: MessageService = MessageService("hellopymsdl_test_rsrc")

        # WHEN
        message: str = message_service.get_message("test_message.txt")

        # THEN
        self.assertEqual("A test message", message)
