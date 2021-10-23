from os import path
from data import Data
import json


class File:
	def __init__(self, file_name: str) -> None:
		self.file_name = file_name

		if path.isfile(file_name) is False or path.getsize(file_name) == 0:
			with open(file_name, 'w') as f:
				json.dump({}, f, indent=4)

	def save(self, name: str, password: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if Data(name).name_to() in data:
				return False

			data[Data(name).name_to()] = Data(password).pass_to()

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def show(self) -> dict:
		result = {}

		with open(self.file_name) as f:
			data = json.load(f)

			for i in data:
				result[Data(i).name_from()] = Data(data[i]).pass_from()

		return result

	def edit_name(self, old_name: str, new_name: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if Data(new_name).name_to() in data or Data(old_name).name_to() not in data:
				return False

			data[Data(new_name).name_to()] = data[Data(old_name).name_to()]
			del data[Data(old_name).name_to()]

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def edit_pass(self, name: str, password: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if Data(name).name_to() not in data:
				return False

			data[Data(name).name_to()] = Data(password).pass_to()

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def delete(self, name: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if Data(name).name_to() in data:
				del data[Data(name).name_to()]

			else:
				return False

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def delete_all(self) -> None:
		with open(self.file_name, 'w') as f:
			json.dump({}, f, indent=4)
