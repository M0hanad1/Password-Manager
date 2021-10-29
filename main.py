from file import File
from os import remove
from json.decoder import JSONDecodeError


class Main:
	def __init__(self, master_file, data_file):
		try:
			self.master_file = File(master_file)
			self.data_file = File(data_file)

			master_check = self.master_file.show()

			if (len(master_check) == 0) or (self.master_file.search('master') is False) or (int(len(master_check['master']) < 6)):
				self.data_file.delete_all()
				self.master_file.delete_all()

		except JSONDecodeError:
			remove('./master.json')
			remove('./data.json')
			print('\nThere\'s a problem with the data files\nPlease try again\n')
			Main('master.json', 'data.json').main()

	def main(self) -> None:
		try:
			if len(self.master_file.show()) == 0:
				print('You don\'t have a master please\nPlease write one')
				master_password = input('Write your master password:\n')

				if len(master_password) < 6 or len(master_password) > 128:
					print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
					return self.main()

				self.master_file.save('master', master_password)
				print(f'\nYour master password is: {master_password}\n')
				return self.master_change()

			if input('Write your master password:\n') == self.master_file.show()['master']:
				print('\nWelcome\n')
				return self.master_change()

			else:
				print('\nThat\'s not your master password\nPlease try again\n')
				return self.main()

		except FileNotFoundError:
			pass

		except JSONDecodeError:
			remove('./master.json')
			remove('./data.json')

		print('\nThere\'s a problem with the data files\nPlease try again\n')
		return Main('master.json', 'data.json').main()

	def master_change(self):
		print('Do you want to change your master password?\n')
		choose = input('Write [Yes, Y] for yes, [N, No] for No:\n').strip().upper()

		if choose == 'YES' or choose == 'Y':
			password = input('\nWrite your new master password:\n')

			if self.master_file.show()['master'] == password:
				print('\nThat\'s your current master password\nPlease Write another one')
				return self.master_change()

			if len(password) < 6 or len(password) > 128:
				print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
				return self.master_change()

			self.master_file.edit_pass('master', password)
			print(f'Your new master password is: {password}')
			return self.run()

		elif choose == 'NO' or choose == 'N':
			print("\nOkay\n")
			return self.run()

		else:
			print("\nWrong value please try again\n")
			return self.master_change()

	def run(self) -> None:
		print('[1, S, Save]: to save a new password')

		if len(self.data_file.show()) > 0:
			print('[2, G, Get]: to get a password\s from the data\n[3, E, Edit]: to edit a password\\name')
			print('[4, D, Delete]: to delete a password\s')

		print('[Q, Quit]: to quit from the program\n')

		choose = input('Choose one of these:\n').strip().upper()

		if choose == '1' or choose == 'S' or choose == 'SAVE':
			name = input('\nWrite the name of the password you want to save it:\n')

			if self.data_file.search(name):
				print(f'\nThere\'s already a password with name {name} in the data\nPlease try again\n')
				return self.run()

			password = input('\nWrite the password:\n')

			if len(password) < 6 or len(password) > 128:
				print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
				return self.run()

			return self.save_password(name, password)

		elif choose == '2' or choose == 'G' or choose == 'GET':
			return self.get_pass(
				input(
					'\nWrite the name of the password you want to get it\nOr write [*] to get all the passwords:\n'
				)
			)

		elif choose == '3' or choose == 'E' or choose == 'EDIT':
			print('\nWrite:\n[1, N, Name]: to edit a name\n[2, P, Password]: to edit a password')
			edit_mode = input('\nChoose one of these:\n').strip().upper()

			if edit_mode == '1' or edit_mode == 'N' or edit_mode == 'NAME':
				old_name = input('\nWrite the old name you want to change from it:\n')

				if self.data_file.search(old_name) is False:
					print(f'\nThere\'s no password with name {old_name} in the data\nPlease try again\n')
					return self.run()

				new_name = input('\nWrite the new name you want to change to it:\n')

				if old_name == new_name:
					print(f'\nThat\'s the same old name\nPlease try again\n')
					return self.run()

				return self.name_edit(old_name, new_name)

			elif edit_mode == '2' or edit_mode == 'P' or edit_mode == 'PASSWORD':
				name = input('\nWrite the name of the password you want to change it:\n')

				if self.data_file.search(name) is False:
					print(f'\nThere\'s no password with name {name} in the data\nPlease try again\n')
					return self.run()

				new_password = input('\nWrite the new password you want to change to it:\n')

				if self.data_file.show()[name] == new_password:
					print('\nThat\'s the same old password\nPlease try again\n')
					return self.run()

				if len(new_password) < 6 or len(new_password) > 128:
					print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
					return self.run()

				return self.pass_edit(name, new_password)

			else:
				print('\nWrong value please try again\n')
				return self.run()

		elif choose == '4' or choose == 'D' or choose == 'DELETE':
			return self.delete_name(
				input(
					'\nWrite the name of the password you want to delete it\nOr write [*] to delete all the passwords:\n'
				)
			)

		elif choose == '5' or choose == 'Q' or choose == 'QUIT':
			quit('\nOkay\nSee you later')

		else:
			print('\nWrong value please try again\n')
			return self.run()

	def save_password(self, name: str, password: str) -> None:
		self.data_file.save(name, password)
		print(f'\nName: {name}\nPassword: {password}\n')
		return self.run()

	def delete_name(self, name: str) -> None:
		if name == '*':
			self.data_file.delete_all()
			return self.run()

		if self.data_file.search(name) is False:
			print(f'\nThere\'s no password with name {name} in the data\nPlease try again\n')
			return self.run()

		self.data_file.delete(name)
		return self.run()

	def name_edit(self, old_name: str, new_name: str) -> None:
		self.data_file.edit_name(old_name, new_name)
		print(f'\nOld name: {old_name}\nNew name: {new_name}\n')
		return self.run()

	def pass_edit(self, name: str, new_password: str) -> None:
		print(f'\nName: {name}\nOld password: {self.data_file.show()[name]}')
		self.data_file.edit_pass(name, new_password)
		print(f'New password: {new_password}\n')

		return self.run()

	def get_pass(self, name: str) -> None:
		if name != '*' and self.data_file.search(name) is False:
			print(f'\nThere\'s no password with name {name} in the data\nPlease try again\n')
			return self.run()

		data = self.data_file.show()

		if name == '*': 
			print('\n')
			[print(f'Name: {i}\nPassword: {data[i]}\n') for i in data]

		else: print(f'\nName: {name}\nPassword: {data[name]}\n')

		return self.run()
