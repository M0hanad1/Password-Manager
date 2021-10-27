from file import File
from os import remove
from json.decoder import JSONDecodeError


class Main:
	def __init__(self, master_file, data_file):
		try:
			self.master_file = File(master_file)
			self.data_file = File(data_file)

			if (len(self.master_file.show()) == 0) or (self.master_file.search('master') is False) or (self.master_file.show()['master'] < 6):
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
					print('\nThe password\'s length should be between 6 and 128 characters')
					print('Please try again\n')
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
				print('\nThat\'s your current master password\nWrite another one')
				return self.master_change()

			if len(password) < 6 or len(password) > 128:
				print('\nThe password\'s length should be between 6 and 128 characters')
				print('Please try again\n')
				return self.master_change()

			self.master_file.edit_pass('master', password)
			print(f'Your new master password is: {password}')

		elif choose == 'NO' or choose == 'N':
			quit('\nOkay')

		else:
			print("\nWrong value please try again\n")
			return self.master_change()

	def save_password(self, name: str, password: str) -> None:
		if self.data_file.search(name):
			print(f'There\'s a password with name {name}\nPlease try again')
			return self.main()

		self.data_file.save(name, password)
		print(f'Name: {name}\nPassword: {password}')
		return self.main()

	def delete_name(self, name: str) -> None:
		if self.data_file.search(name):
			self.data_file.delete(name)
			return self.main

		return self.main()
