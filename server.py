import socketserver
from hashlib import sha256
from model import TPM
from pwn import *
import pickle

# Neural network setting
hidden_layer = 20
input_layer = 5
max_value = 6

# All possible update rules
update_rules = ["hebbian", "anti_hebbian", "random_walk"]


class TCPHandler(socketserver.BaseRequestHandler):
    """
        Class for TCP server for neural network synchronization.
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

                server_tpm = TPM(input_layer, hidden_layer, max_value)
                sync = False

                while not sync:
                    input_val = pickle.loads(r.readline(keepends=False, timeout=2))
                    server_output = server_tpm(input_val)
                    r.sendline(str(server_output).encode())
                    client_output = float(r.readline(keepends=False, timeout=2).decode("utf-8"))
                    server_tpm.update(client_output, update_rule)

                    if server_output == client_output:
                        client_hash = r.readline(keepends=False, timeout=2).decode("utf-8")
                        server_hash = sha256(pickle.dumps(server_tpm.weights)).hexdigest()
                        r.sendline(server_hash.encode())
                        if client_hash == server_hash:
                            input_data = r.recvline(keepends=False, timeout=2).decode("utf-8")
                            sync = True
                            print("Machines have been synchronized.")


def start(host="192.168.2.46", port=9999):
    """
    Function for starting TCP server

    :param host: sever address
    :type host: str
    :param port: port number
    :type port: int
    """

    print("Server started.")
    with socketserver.TCPServer((host, port), TCPHandler) as bob_server:
        bob_server.serve_forever()


if __name__ == '__main__':
    start()
