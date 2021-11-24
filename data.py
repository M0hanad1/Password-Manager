from base64 import b85encode, b85decode
from typing import Union


class Data:
    def __init__(self, target: Union[str, list]) -> None:
        self.target = target

    def pass_to(self) -> list:
        return [ord(self.target[i]) for i in range(len(self.target))]

    def pass_from(self) -> str:
        return "".join([chr(self.target[i]) for i in range(len(self.target))])

    def name_to(self) -> str:
        return str(b85encode(bytes(self.target, 'utf-8')))[2:-1]

    def name_from(self) -> str:
        return str(b85decode(bytes(self.target, 'utf-8')))[2:-1]
