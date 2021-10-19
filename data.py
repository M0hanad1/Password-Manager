from os import path
import json


class Data:
	def __init__(self, file_name: str) -> None:
		self.file_name = file_name

		if path.isfile(file_name) is False or path.getsize(file_name) == 0:
			with open(file_name, 'w') as f:
				json.dump({}, f, indent=4)

	@staticmethod
	def convert_to(string: str) -> list:
		return [ord(i) for i in string]

	@staticmethod
	def convert_from(lst: list) -> str:
		return "".join([chr(i) for i in lst])


	def save(self, name: str, password: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if name in data:
				return False

			data[name] = self.convert_to(password)

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def show(self) -> dict:
		result = {}

		with open(self.file_name) as f:
			data = json.load(f)

			for i in data:
				result[i] = self.convert_from(data[i])

		return result

	def edit_name(self, old_name: str, new_name: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if new_name in data or old_name not in data:
				return False

			data[new_name] = data[old_name]
			del data[old_name]

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def edit_pass(self, name: str, password: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if name not in data:
				return False

			data[name] = self.convert_to(password)

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def delete(self, name: str) -> bool:
		with open(self.file_name) as f:
			data = json.load(f)

			if name in data:
				del data[name]

			else:
				return False

		with open(self.file_name, 'w') as d:
			json.dump(data, d, indent=4)

		return True

	def remove_all(self) -> None:
		with open(self.file_name, 'w') as f:
			json.dump({}, f, indent=4)
