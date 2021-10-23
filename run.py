from main import Main


if __name__ == '__main__':
    try:
        Main('master.json', 'data.json').main()
    except FileNotFoundError:
        print('\nThere\'s a problem with the data files\nPlease try again\n')

    Main('master.json', 'data.json').main()
