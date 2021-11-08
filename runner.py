from main import Main
from os import getenv


if __name__ == '__main__':
    if getenv('APPDATA') is None:
        Main('./PassData', '/master.json', '/data.json').main()

    Main(getenv('APPDATA') + '/PassData', '/master.json', '/data.json').main()
