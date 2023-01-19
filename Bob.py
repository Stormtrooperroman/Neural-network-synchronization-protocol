import socketserver
from hashlib import sha256
from model import TPM
from pwn import *
import pickle

update_rules = ["hebbian", "anti_hebbian", "random_walk"]

hidden_layer = 20
input_layer = 5
max_value = 6


class TCPHandler(socketserver.BaseRequestHandler):
    """
        Function for TCP server for neural network synchronization.
    """
    def handle(self):
        r = remote.fromsocket(self.request)
        input_data = r.recvline(keepends=False, timeout=2).decode("utf-8")
        print(f"{self.client_address[0]} wrote:")

        if input_data.lower() == "start synchronization":
            r.sendline("ok".encode())
            rule = r.recvline(keepends=False, timeout=2).decode("utf-8")
            if rule in update_rules:
                update_rule = update_rules[update_rules.index(rule)]

                Bob = TPM(input_layer, hidden_layer, max_value)
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
    print("Bob started.")
    with socketserver.TCPServer((host, port), TCPHandler) as bob_server:
        bob_server.serve_forever()


if __name__ == '__main__':
    start()
