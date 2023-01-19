import numpy as np
from model import TPM
from hashlib import sha256
from pwn import *
import pickle
from time import time

hidden_layer = 20
input_layer = 5
max_value = 6


def random():
    """
    Function for generate input arrays.
    """

    return np.random.randint(-max_value, max_value+1, [hidden_layer, input_layer])


update_rules = ["hebbian", "anti_hebbian", "random_walk"]
update_rule = update_rules[0]


def synchronization(host="localhost", port=9999):
    """
    Function for connect to server and neural network synchronization

    :param host: sever address
    :type host: str
    :param port: port number
    :type port: int
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    r = remote.fromsocket(s)
    r.sendline("start synchronization".encode())
    data_input = r.recvline(keepends=False, timeout=2).decode("utf-8")
    if data_input.lower() == "ok":

        r.sendline(f"{update_rule}".encode())
        Alice = TPM(input_layer, hidden_layer, max_value)

        sync = False
        nb_updates = 0
        start_time = time()

        while not sync:
            input_val = random()
            tauA = Alice(input_val)
            r.sendline(pickle.dumps(input_val))
            tauB = float(r.readline(keepends=False, timeout=2).decode("utf-8"))
            r.sendline(str(tauA).encode())
            Alice.update(tauB, update_rule)
            nb_updates += 1
            alice_hash = sha256(pickle.dumps(Alice.weights)).hexdigest()
            r.sendline(alice_hash.encode())
            bob_hash = r.readline(keepends=False, timeout=2).decode("utf-8")

            if alice_hash == bob_hash:
                sync = True
                end_time = time()
                time_taken = end_time - start_time
                print("Machines have been synchronized.")
                print(f"Updates = {nb_updates}.")
                print(f"Time taken = {time_taken} seconds.")

    s.close()


if __name__ == "__main__":
    synchronization()
