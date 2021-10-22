from base64 import b85encode, b85decode


class Data:
    def __init__(self, target: str | list) -> None:
        self.target = target

    def pass_to(self) -> list:
        return [ord(self.target[i]) for i in range(len(self.target))]

    def pass_from(self) -> str:
        return "".join([chr(self.target[i]) for i in range(len(self.target))])

    def name_to(self) -> list:
        message_bytes = self.target.encode('ascii')
        base64_bytes = b85encode(message_bytes)
        return base64_bytes.decode('ascii')

    def name_from(self) -> str:
        base64_bytes = self.target.encode('ascii')
        message_bytes = b85decode(base64_bytes)
        return message_bytes.decode('ascii')
