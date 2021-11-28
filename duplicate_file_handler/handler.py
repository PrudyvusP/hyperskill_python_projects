import argparse
import hashlib
import os
import sys
import typing
from collections import defaultdict

CHOOSE_FORMAT = 'Enter file format:\n'
CHOOSE_SORT = 'Enter a sorting option:\n'

DUPLICATE_QUESTION = 'Check for duplicates?\n'
DELETE_QUESTION = 'Delete files?\n'
WHICH_FILES_QUESTION = 'Enter nums of files which should be removed? (i.e. 1 2 4 etc)\n'

WRONG_OPTION_INFO = 'Wrong option\n'
WRONG_FORMAT_INFO = 'Wrong format\n'

SORTING_VARIETY = 'Size sorting options:\n1. Descending\n2. Ascending'
SORT_OPTIONS = ('1', '2')
YES_OPTIONS = ('yes', 'y', 'yeah', 'ya')
NO_OPTIONS = ('no', 'n', 'nope', 'never')

SORT_CONST = 2
BYTES_CONST = 8192


def parse_args() -> str:
    """Returns parsed arg with a directory"""
    parser = argparse.ArgumentParser(description='Duplicate File Handler')
    parser.add_argument('directory',
                        type=str,
                        help='which directory should handler start doing job')
    args = parser.parse_args()
    return args.directory


def read_sort_option() -> int:
    """Check sort option and returns valid num"""
    print(SORTING_VARIETY)
    while True:
        choice = input(CHOOSE_SORT)
        if choice not in SORT_OPTIONS:
            print(WRONG_OPTION_INFO)
        else:
            break
    return int(choice)


def get_file_hash(_file_name: str) -> str:
    """Returns the hash of file's data"""
    with open(_file_name, mode='rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(BYTES_CONST):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def get_dir_info(_dir: str, ending: str) -> typing.Tuple[dict, dict]:
    """Returns two dicts with info data after walking through the directory"""
    _dct_sizes_names = defaultdict(list)
    _dct_sizes_hash_names = defaultdict(list)
    if os.access(_dir, os.R_OK):
        for root, dirs, files in os.walk(_dir, topdown=True):
            for name in files:
                file_name = os.path.join(root, name)
                if file_name.endswith(ending):
                    _size = os.path.getsize(file_name)
                    _hash = get_file_hash(file_name)
                    _dct_sizes_names[_size].append(file_name)
                    _dct_sizes_hash_names[(_size, _hash)].append(file_name)
    return _dct_sizes_names, _dct_sizes_hash_names


def get_structed_info(_dct_sizes_names: dict, _dct_sizes_hash_names: dict) -> dict:
    """Returns all info about data in the structed dict"""
    _dct_main = defaultdict(list)
    for main_size_key in _dct_sizes_names:
        for main_size_hash_key in _dct_sizes_hash_names:
            if main_size_key == main_size_hash_key[0]:
                _dct_main[main_size_key].append({
                    'hash': main_size_hash_key[1],
                    'files': _dct_sizes_hash_names[main_size_hash_key]
                })
    return _dct_main


def print_file_sizes(_dct_main: dict, _sorting_option: int) -> None:
    """Prints info about each file and it's size"""
    for k in sorted(_dct_main, reverse=bool(_sorting_option < SORT_CONST)):
        print(k, 'bytes')
        for value in _dct_main[k]:
            print(*value['files'], sep='\n')


def search_for_duplicates(_dct_main: dict, _sorting_option: int) -> list:
    """Returns a list of duplicates file names and their sizes"""
    while True:
        duplicate_option = input(DUPLICATE_QUESTION).lower()
        if duplicate_option in YES_OPTIONS:
            counter = 1
            container_with_duplicates = []
            for size in sorted(_dct_main, reverse=bool(_sorting_option < SORT_CONST)):
                for hash_files in _dct_main[size]:
                    if len(hash_files['files']) > 1:
                        print('Hash:', hash_files['hash'])
                        for file in hash_files['files']:
                            print(f'{counter}. [{size} bytes] {file}')
                            container_with_duplicates.append((file, size))
                            counter += 1
            break
        elif duplicate_option in NO_OPTIONS:
            break
        else:
            print(WRONG_OPTION_INFO)
    return container_with_duplicates


def delete_duplicates(_container: list) -> None:
    """Deletes duplicate files and printing results info"""
    while True:
        delete_option = input(DELETE_QUESTION).lower()
        if delete_option in YES_OPTIONS:
            print(WHICH_FILES_QUESTION)
            what_files = input()
            if (what_files.replace(' ', '').isdigit()
                    and set(map(int, what_files.split())).issubset(list(range(1, len(_container) + 1)))):
                nums_for_del = map(int, what_files.split())
                memory_free = 0
                for num in nums_for_del:
                    os.remove(_container[num - 1][0])
                    memory_free += _container[num - 1][1]
                print(f'Total freed up space:\n{memory_free} bytes')
            else:
                print(WRONG_FORMAT_INFO)
            break
        elif delete_option in NO_OPTIONS:
            sys.exit()
        else:
            print(WRONG_OPTION_INFO)


def main() -> None:
    """The main function (a controller)"""
    root_d = parse_args()
    _format = input(CHOOSE_FORMAT)
    sorting_option = read_sort_option()
    data = get_dir_info(root_d, _format)
    dct_sizes_names, dct_sizes_hash_names = data[0], data[1]
    dct_main = get_structed_info(dct_sizes_names, dct_sizes_hash_names)
    print_file_sizes(dct_main, sorting_option)
    container = search_for_duplicates(dct_main, sorting_option)
    delete_duplicates(container)


if __name__ == '__main__':
    main()
