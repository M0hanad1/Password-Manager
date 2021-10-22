from file import File

class Main:
	def __init__(self, master_file, File_file):
		self.master_file = File(master_file)
		self.file_file = File(File_file)

		if bool(self.master_file.show()) is False:
			if bool(self.file_file.show()):
				self.file_file.remove_all()

	def main(self):
		if bool(self.master_file.show()) is False:
			print('You don\'t have a master please\nPlease write one')
			master_password = input('Write your master password:\n')

			if len(master_password) == 0:
				print('\nPleae Write your master password\n')

			self.master_file.save('master', master_password)
			print(f'\nYour master password is {master_password}\n')
			return self.master_change()

		else:
			master_password = input('Write your master password:\n')

			if master_password == self.master_file.show()['master']:
				print('\nWelcome\n')
				return self.master_change()

			else:
				print('\nThat\'s not your master password\nPlease try again\n')

		return self.main()

	def master_change(self):
		print('Do you want to change your master password?\n')
		choose = input('Write [Yes, Y] for yes, [N, No] for No:\n').upper()

		if choose == 'YES' or choose == 'Y':
			password = input('\nWrite your new master password:\n')

			if self.master_file.show()['master'] == password:
				print('\nThat\'s your current master file\nWrite another one')
				return self.master_change()

			self.master_file.edit_pass('master', password)
			print(f'Your new master password is {password}')


		elif choose == 'NO' or choose == 'N':
			print('\nOkay\n')

		else:
			print("\nWrong value please try again\n")
			return self.master_change()
