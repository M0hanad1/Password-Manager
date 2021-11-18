from file import File
from os import path, mkdir, remove
from json.decoder import JSONDecodeError
from string import ascii_uppercase, ascii_lowercase, punctuation, digits
from random import choice, shuffle


class Main:
	def __init__(self, folder: str, master_file: str, data_file: str) -> None:
		if path.exists(folder) is False:
			mkdir(folder)

		self.folder = folder
		self.master_file = File(folder + master_file)
		self.data_file = File(folder + data_file)

		try:
			check = self.master_file.show()

			if len(check) == 0 or len(check['master']) < 6:
				self.master_file.delete_all()
				self.data_file.delete_all()

		except JSONDecodeError:
			remove(folder + master_file)
			remove(folder + data_file)
			print('\nThere\'s a problem with the data files\nPlease try again\n')
			Main(folder, master_file, data_file).main()

		try:
			self.data_file.search('test')

		except JSONDecodeError:
			remove(folder + data_file)
			print('\nThere\'s a problem with the data files\nPlease try again\n')
			Main(folder, master_file, data_file).main()

	@staticmethod
	def check(string: str) -> list:
		result = []

		for i in range(len(string)):
			if (string[i] == '1' or string[i] == 'U') and ascii_uppercase not in result:
				result.append(ascii_uppercase)

			elif (string[i] == '2' or string[i] == 'L') and ascii_lowercase not in result:
				result.append(ascii_lowercase)

			elif (string[i] == '3' or string[i] == 'D') and digits not in result:
				result.append(digits)

			elif (string[i] == '4' or string[i] == 'P') and punctuation not in result:
				result.append(punctuation)

		return result

	@staticmethod
	def generate(password_len: int, lst: list) -> str:
		password = []
		index = 0

		try:
			while len(password) < password_len:
				[(password.append(choice(lst[index]))) for _ in range(password_len // len(lst))]
				index += 1

		except IndexError:
			[password.append(choice(choice(lst))) for _ in range(password_len - len(password))]

		shuffle(password)
		return ''.join(password)

	def main(self) -> None:
		try:
			if len(self.master_file.show()) == 0:
				print('You don\'t have a master password\nPlease write one')
				master_password = input('Write your master password:\n')

				if len(master_password) < 6 or len(master_password) > 128:
					print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
					return self.main()

				if input('\nWrite the password again:\n') != master_password:
					print('\nThat\'s not the same password\nPlease try again\n')
					return self.main()

				self.master_file.save('master', master_password)
				print(f'\nYour master password is: {master_password}\n')
				return self.master_change()

			if input('Write your master password:\n') == self.master_file.show()['master']:
				print('\nWelcome\n')
				return self.master_change()

			print('\nThat\'s not your master password\nPlease try again\n')
			return self.main()

		except FileNotFoundError:
			print('\nThere\'s a problem with the data files\nPlease try again\n')

		except JSONDecodeError:
			pass

		return Main(self.folder, '/master.json', '/data.json').main()

	def master_change(self) -> None:
		print('Do you want to change your master password?')
		choose = input('Write [1, Y, Yes] for yes, [2, N, No] for No:\n').strip().upper()

		if choose == '1' or choose == 'YES' or choose == 'Y':
			password = input('\nWrite your new master password:\n')

			if self.master_file.show()['master'] == password:
				print('\nThat\'s your current master password\nPlease Write another one\n')
				return self.master_change()

			if len(password) < 6 or len(password) > 128:
				print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
				return self.master_change()

			if input('\nWrite the password again:\n') != password:
				print('\nThat\'s not the same password\nPlease try again\n')
				return self.master_change()

			self.master_file.edit_pass('master', password)
			print(f'\nYour new master password is: {password}\n')
			return self.run()

		elif choose == '2' or choose == 'NO' or choose == 'N':
			print("\nOkay\n")
			return self.run()

		else:
			print("\nWrong value please try again\n")
			return self.master_change()

	def run(self) -> None:
		check = False

		if len(self.data_file.show()) > 0:
			check = True

		print('[1, S, Save]: to save a new password\n[2, M, Make]: to generate a random password')

		if check:
			print(
				'[3, G, Get]: to get a password\\s from the data\n[4, E, Edit]: to edit a password\\name'
				'\n[5, D, Delete]: to delete a password\\s'
			)

		print('[Q, Quit]: to quit from the program\n')

		choose = input('Choose one of these:\n').strip().upper()

		if choose == '1' or choose == 'S' or choose == 'SAVE':
			name = input('\nWrite the name of the password you want to save it:\n').lower()

			if len(name) < 2 or len(name) > 64:
				print('\nThe name\'s length should be between 3 and 64 characters\nPlease try again\n')
				return self.run()

			if self.data_file.search(name):
				print(f'\nThere\'s already a password with name "{name}" in the data\nPlease try again\n')
				return self.run()

			password = input('\nWrite the password:\n')

			if len(password) < 6 or len(password) > 128:
				print('\nThe password\'s length should be between 6 and 128 characters\nPlease try again\n')
				return self.run()

			return self.save_password(name, password)

		elif choose == '2' or choose == 'M' or choose == 'MAKE':
			return self.ask(self.generate_pass())

		elif choose == 'Q' or choose == 'QUIT':
			quit('\nOkay\nSee you later')

		else:
			if check:
				if choose == '3' or choose == 'G' or choose == 'GET':
					return self.get_pass(
						input(
							'\nWrite the name of the password you want to get it\n'
							'Or write [*] to get all the passwords:\n'
						).lower()
					)

				elif choose == '4' or choose == 'E' or choose == 'EDIT':
					print('\nWrite:\n[1, N, Name]: to edit a name\n[2, P, Password]: to edit a password')
					edit_mode = input('\nChoose one of these:\n').strip().upper()

					if edit_mode == '1' or edit_mode == 'N' or edit_mode == 'NAME':
						old_name = input('\nWrite the old name you want to change from it:\n').lower()

						if self.data_file.search(old_name) is False:
							print(f'\nThere\'s no password with name "{old_name}" in the data\nPlease try again\n')
							return self.run()

						new_name = input('\nWrite the new name you want to change to it:\n').lower()

						if self.data_file.search(new_name):
							print(f'\nThere\'s already a password with name "{new_name}" on the data\nPlease try again\n')
							return self.run()

						if old_name == new_name:
							print(f'\nThat\'s the same old name\nPlease try again\n')
							return self.run()

						if len(new_name) < 2 or len(new_name) > 64:
							print('\nThe name\'s length should be between 3 and 64 characters\nPlease try again\n')
							return self.run()

						return self.name_edit(old_name, new_name)

					elif edit_mode == '2' or edit_mode == 'P' or edit_mode == 'PASSWORD':
						name = input('\nWrite the name of the password you want to change it:\n').lower()

						if self.data_file.search(name) is False:
							print(f'\nThere\'s no password with name "{name}" in the data\nPlease try again\n')
							return self.run()

						mode = input(
									'\nDo you want to write the password by yourself or you want to generate it?\n'
									'Write:\n[1, W, Write]: To write the password by yourself\n[2, G, Generate]: To'
									' generate a random password\n'
								).strip().upper()

						if mode == '1' or mode == 'W' or mode == 'WRITE':
							new_password = input('\nWrite the new password you want to change to it:\n')

							if self.data_file.show()[name] == new_password:
								print('\nThat\'s the same old password\nPlease try again\n')
								return self.run()

							if len(new_password) < 6 or len(new_password) > 128:
								print(
									'\nThe password\'s length should be between 6 and 128 characters\n'
									'Please try again\n'
								)
								return self.run()

							return self.pass_edit(name, new_password)

						elif mode == '2' or mode == 'G' or mode == 'GENERATE':
							return self.random_edit(name, self.generate_pass())

						else:
							print('\nWrong value please try again\n')
							return self.run()

					else:
						print('\nWrong value please try again\n')
						return self.run()

				elif choose == '5' or choose == 'D' or choose == 'DELETE':
					return self.delete_name(
						input(
							'\nWrite the name of the password you want to delete it\n'
							'Or write [*] to delete all the passwords:\n'
						).lower()
					)

			else:
				print('\nWrong value please try again\n')
				return self.run()

	def ask(self, string: str) -> None:
		print(f'\nYour random password is: {string}\nDo you want to save it?\n')
		choose = input('Write [1, Y, Yes] for yes, [2, N, No] for No:\n').strip().upper()

		if choose == '1' or choose == 'Y' or choose == 'YES':
			name = input('\nWrite the name of the password you want to save it:\n').lower()

			if len(name) < 2 or len(name) > 64:
				print('\nThe name\'s length should be between 3 and 64 characters\nPlease try again')
				return self.ask(string)

			if self.data_file.search(name):
				print(f'\nThere\'s already a password with name "{name}" in the data\nPlease try again')
				return self.ask(string)

			return self.save_password(name, string)

		elif choose == '2' or choose == 'N' or choose == 'NO':
			print('\nOkay\n')
			return self.run()

		else:
			print('\nWrong value please try again')
			return self.ask(string)

	def save_password(self, name: str, password: str) -> None:
		self.data_file.save(name, password)
		print(f'\nName: {name}\nPassword: {password}\n')
		return self.run()

	def delete_name(self, name: str) -> None:
		if name == '*':
			self.data_file.delete_all()
			print('\nDone\n')
			return self.run()

		if self.data_file.search(name) is False:
			print(f'\nThere\'s no password with name "{name}" in the data\nPlease try again\n')
			return self.run()

		self.data_file.delete(name)
		print('\nDone\n')
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

	def random_edit(self, name: str, random_pass) -> None:
		print(f'\nYour random password is: {random_pass}\n\nDo you want to save it?')
		save_or_no = input('Write:\n[1, Y, Yes]: for yes\n[2, N, No]: for no\n').strip().upper()

		if save_or_no == '1' or save_or_no == 'Y' or save_or_no == 'YES':
			return self.pass_edit(name, random_pass)

		elif save_or_no == '2' or save_or_no == 'N' or save_or_no == 'NO':
			print('\nDo you want to try to generate another password?')
			try_again = input('Write:\n[1, Y, Yes]: for yes\n[2, N, No]: for no\n')

			if try_again == '1' or try_again == 'Y' or try_again == 'YES':
				return self.random_edit(name, self.generate_pass())

			elif try_again == '2' or try_again == 'N' or try_again == 'NO':
				print('\nOkay\n')
				return self.run()

			else:
				print('\nWrong value please try again\n')
				return self.random_edit(name, random_pass)

		else:
			print('\nWrong value please try again\n')
			return self.random_edit(name, random_pass)

	def get_pass(self, name: str) -> None:
		if name != '*' and self.data_file.search(name) is False:
			print(f'\nThere\'s no password with name "{name}" in the data\nPlease try again\n')
			return self.run()

		data = self.data_file.show()

		if name == '*':
			print('')
			[print(f'Name: {i}\nPassword: {data[i]}\n') for i in data]

		else:
			print(f'\nName: {name}\nPassword: {data[name]}\n')

		return self.run()

	def generate_pass(self) -> str:
		print(
				'\nChoose what you want your password to have\n[1, U]: For uppercase letters\n[2, L]: For lowercase letters'
				'\n[3, D]: For digits (Numbers)\n[4, P]: For punctuation\nIf you want to choose a multiple choices you can '
				'just write it like this:\n124 or ULP\n\nWrite [E, Exit]: to exit from random generate mode\n'
			)

		choose = input('Choose from these:\n').strip().upper()

		if choose == 'E' or choose == 'EXIT':
			print('\nOkay\n')
			return self.run()

		lst_choose = self.check(choose)

		if len(lst_choose) == 0:
			print('\nWrong value please try again\n')
			return self.generate_pass()

		try:
			pass_len = int(input('\nWrite the size of the password\nShould be between 6 and 128:\n'))

			if pass_len < 6 or pass_len > 128:
				print('\nThe password size should be between 6 and 128\nPlease try again\n')
				return self.generate_pass()

		except ValueError:
			print('\nWrong value please try again\n')
			return self.generate_pass()

		return self.generate(pass_len, lst_choose)
