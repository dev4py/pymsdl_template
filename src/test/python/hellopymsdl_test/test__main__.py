"""Main file tests"""
from typing import Final
from unittest.mock import patch, MagicMock, call
from runpy import run_module


class TestHello:
    """hello function Tests"""

    class TestNominalCase:

        @patch('hellopymsdl.service.MessageService.MessageService')
        @patch('builtins.print')
        def test_call_hello__should__print_message_from_message_service(
                self, print_mock: MagicMock, message_service_mock: MagicMock
        ) -> None:
            """When call hello function from main, should print the message service message"""
            # GIVEN
            test_message: Final[str] = "My test message"
            message_service_mock.return_value.get_message.return_value = test_message

            # WHEN
            from hellopymsdl.__main__ import hello
            hello()

            # THEN
            assert message_service_mock.return_value.get_message.call_count == 1
            assert print_mock.call_count == 2
            print_mock.assert_has_calls([
                call("hello python with Maven Standard Directory Layout"),
                call(test_message),
            ])
