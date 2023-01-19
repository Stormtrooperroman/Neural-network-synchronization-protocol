import socketserver
from hashlib import sha256
import time
from model import TPM
from pwn import *
import pickle


def recv_timeout(the_socket, timeout=2):
    the_socket.setblocking(0)

    total_data = []
    data = ''

    begin = time.time()
    while 1:
        if total_data and time.time() - begin > timeout:
            break

        elif time.time() - begin > timeout * 2:
            break

        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data.decode("utf-8"))
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass

    return ''.join(total_data)


update_rules = ["hebbian", "anti_hebbian", "random_walk"]

k = 20
n = 5
l = 6


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        r = remote.fromsocket(self.request)
        input_data = r.recvline(keepends=False, timeout=2).decode("utf-8")
        print(f"{self.client_address[0]} wrote:")

        if input_data.lower() == "start synchronization":
            r.sendline("ok".encode())
            rule = r.recvline(keepends=False, timeout=2).decode("utf-8")
            if rule in update_rules:
                update_rule = update_rules[update_rules.index(rule)]

                Bob = TPM(n, k, l)
                sync = False

                while not sync:

                    input_val = pickle.loads(r.readline(keepends=False, timeout=2))
                    tauB = Bob(input_val)
                    r.sendline(str(tauB).encode())
                    tauA = float(r.readline(keepends=False, timeout=2).decode("utf-8"))
                    Bob.update(tauA, update_rule)
                    alice_hash = r.readline(keepends=False, timeout=2).decode("utf-8")
                    bob_hash = sha256(pickle.dumps(Bob.weights)).hexdigest()
                    r.sendline(bob_hash.encode())
                    if alice_hash == bob_hash:
                        sync = True
                        print("Machines have been synchronized.")


def start(host="localhost", port=9999):
    HOST, PORT = host, port
    print("Bob started.")
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    start()
