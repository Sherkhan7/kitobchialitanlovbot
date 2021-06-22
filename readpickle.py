import pickle
import sys
from pprint import pp

from config import PICKLE_FILE_NAME


def read_data():
    filename = f'{PICKLE_FILE_NAME}_{sys.argv[-1]}'
    loaded_file = pickle.load(open(f'{filename}', 'rb'))

    pp(''.ljust(100, '-'))
    pp(loaded_file)
    pp(''.ljust(100, '-'))


if __name__ == '__main__':
    read_data()
