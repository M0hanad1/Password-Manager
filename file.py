from os import path
from data import Data
from json import load, dump


class File:
	def __init__(self, file_name: str) -> None:
		self.file_name = file_name

		if path.isfile(file_name) is False or path.getsize(file_name) == 0:
			with open(file_name, 'w') as f:
				dump({}, f, indent=4)

	def search(self, name: str) -> bool:
		with open(self.file_name) as f:
			data = load(f)

		return Data(name).name_to() in data

	def save(self, name: str, password: str) -> None:
		with open(self.file_name) as f:
			data = load(f)
			data[Data(name).name_to()] = Data(password).pass_to()

		with open(self.file_name, 'w') as d:
			dump(data, d, indent=4)

	def show(self) -> dict:
		with open(self.file_name) as f:
			data = load(f)
			return {Data(i).name_from(): Data(data[i]).pass_from() for i in data}

	def edit_name(self, old_name: str, new_name: str) -> None:
		with open(self.file_name) as f:
			data = load(f)

			data[Data(new_name).name_to()] = data[Data(old_name).name_to()]
			del data[Data(old_name).name_to()]

		with open(self.file_name, 'w') as d:
			dump(data, d, indent=4)

	def edit_pass(self, name: str, password: str) -> None:
		with open(self.file_name) as f:
			data = load(f)
			data[Data(name).name_to()] = Data(password).pass_to()

		with open(self.file_name, 'w') as d:
			dump(data, d, indent=4)

	def delete(self, name: str) -> None:
		with open(self.file_name) as f:
			data = load(f)
			del data[Data(name).name_to()]

		with open(self.file_name, 'w') as d:
			dump(data, d, indent=4)

	def delete_all(self) -> None:
		with open(self.file_name, 'w') as f:
			dump({}, f, indent=4)
