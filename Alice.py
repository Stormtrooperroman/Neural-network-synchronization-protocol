import numpy as np
import time
from model import TPM
from hashlib import sha256
from pwn import *
import pickle

def random():
    return np.random.randint(-l, l+1, [k, n])


update_rules = ["hebbian", "anti_hebbian", "random_walk"]
update_rule = update_rules[0]

k = 20
n = 5
l = 6


def synchronization(host="localhost", port=9999):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    r = remote.fromsocket(s)
    r.sendline("start synchronization".encode())
    data_input = r.recvline(keepends=False, timeout=2).decode("utf-8")
    if data_input.lower() == "ok":

        r.sendline(f"{update_rule}".encode())
        Alice = TPM(n, k, l)

        sync = False
        nb_updates = 0
        start_time = time.time()
        sync_history = []

        while not sync:
            input_val = random()
            tauA = Alice(input_val)
            r.sendline(pickle.dumps(input_val))
            tauB = float(r.readline(keepends=False, timeout=2).decode("utf-8"))
            r.sendline(str(tauA).encode())
            Alice.update(tauB, update_rule)
            nb_updates += 1
            alice_hash = sha256(pickle.dumps(Alice.weights)).hexdigest()
            print(alice_hash)
            r.sendline(alice_hash.encode())
            bob_hash = r.readline(keepends=False, timeout=2).decode("utf-8")

            if alice_hash == bob_hash:
                sync = True
                print("Machines have been synchronized.")
                print(f"Updates = {nb_updates}.")

    s.close()


if __name__ == "__main__":
    synchronization()
