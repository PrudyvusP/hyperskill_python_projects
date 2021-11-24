import argparse
import os
import re
import sys

import requests
from bs4 import BeautifulSoup, ResultSet
from colorama import Fore


def check_valid_url(strq: str) -> bool:
    """Returns True if there is a dot in the string"""
    return bool(re.search(r'\.', strq))


def add_protocol(strq: str) -> str:
    """Returns a valid URL if it is not"""
    if not strq.startswith('https://'):
        strq = 'https://' + strq
    return strq


def parse_response(request: str) -> ResultSet:
    """Returns bs4 additional list with results of parsing"""
    try:
        r = requests.get(request)
    except requests.exceptions.SSLError:
        print('HTTPS ONLY')
        sys.exit()
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.find_all([
        'p', 'h1', 'h2', 'h3', 'h4',
        'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    return text


def print_results(lst_with_text: ResultSet) -> None:
    """Prints blue colored hrefs whereas simple text with custom color"""
    print(*[Fore.BLUE + i.text.strip()
            if i.name == 'a'
            else Fore.RESET + i.text.strip() for i in lst_with_text],
          sep='\n')


def cut_root_domain(strq: str) -> str:
    """Returns a domain name without a root domain"""
    return strq[:strq.rfind('.')]


def write_to_file(file_name: str, lst_with_text) -> None:
    """Creates a file with parsed text close to cache-idea"""
    with open(file_name, 'w', encoding='utf-8') as w_f:
        for text in lst_with_text:
            w_f.write(text.text.strip() + '\n')


def read_data_from_file(file_name: str) -> None:
    """Reads some data from a file"""
    with open(file_name, 'r') as f:
        print(*[i for i in f.read()], sep='')


parser = argparse.ArgumentParser(description='Little Text browser')
parser.add_argument('folder_name',
                    type=str,
                    help='name of the folder to store text data from sites')
args = parser.parse_args()
request = args.folder_name
dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       request)

stack = []  # to have an opportunity to go back

if __name__ == '__main__':
    """Controller of the program"""
    os.makedirs(dirname, exist_ok=True)
    dir_lst = os.listdir(dirname)

    while True:
        request = input()

        if request == 'exit':
            break
        else:
            if request in dir_lst:
                read_data_from_file(os.path.join(dirname, request))
                continue

        if request == 'back':
            if stack:
                stack.pop()
                if stack:
                    read_data_from_file(stack[-1])
                    continue

        if not check_valid_url(request):
            print('Incorrect URL')
        else:
            filename = os.path.join(dirname, cut_root_domain(request))
            stack.append(filename)
            request = add_protocol(request)
            text_lst = parse_response(request)
            print_results(text_lst)
            write_to_file(file_name=filename, lst_with_text=text_lst)
