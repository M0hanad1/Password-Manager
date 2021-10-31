from main import Main
from os import getenv


if __name__ == '__main__':
    Main(getenv('APPDATA') + '/PassData', '/master.json', '/data.json').main()
