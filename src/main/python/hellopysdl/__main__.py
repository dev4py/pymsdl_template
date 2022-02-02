from hellopysdl.service.MessageService import MessageService


def hello() -> None:
    print("hello python Standard Directory Layout")
    message_service: MessageService = MessageService(message_file_name="message.txt")
    print(message_service.get_message())


if __name__ == '__main__':
    hello()
