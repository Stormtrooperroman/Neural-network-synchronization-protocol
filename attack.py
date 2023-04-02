from scapy.all import *
from model import TPM
import pickle
from hashlib import sha256

all_data = {}

hidden_layer = 20
input_layer = 5
max_value = 6
update_rules = ["hebbian", "anti_hebbian", "random_walk"]


def synchronization(data):
    update_rule = update_rules[update_rules.index(data[1].decode("utf-8").strip())]
    attack_tpm = TPM(input_layer, hidden_layer, max_value)
    i = 2
    while i < len(data[2:]):
        input_val = pickle.loads(data[i])
        i += 1
        server_output = float(data[i].decode("utf-8").strip())
        i += 1
        client_output = float(data[i].decode("utf-8").strip())
        if client_output == server_output:
            attack_output = attack_tpm(input_val)
            i += 1
            client_hash = data[i].decode("utf-8").strip()
            i += 1
            server_hash = data[i].decode("utf-8").strip()
            if attack_output == client_output:
                attack_tpm.update(client_output, update_rule)
            if server_hash == client_hash:
                attack_hash = sha256(pickle.dumps(attack_tpm.weights)).hexdigest()
                if server_hash == attack_hash:
                    print("The attack was successful. Managed to get the weight.")
                else:
                    print("The machines synchronized before the attack succeeded.")
                return
        i += 1


def simple_attack(pkt):
    if Raw in pkt:
        data = pkt[Raw].load
        str_data = ""
        try:
            str_data = data.decode("utf-8").split("\n")[0]
        except:
            pass
        src = pkt.sprintf("{IP:%IP.src%:%IP.dport%}")
        dst = pkt.sprintf("{IP:%IP.dst%:%IP.sport%}")
        if str_data == "start synchronization":
            all_data[dst] = []

        elif str_data == "finish synchronization":
            print("HAHAHA")
            if src in all_data:
                all_data[src].append(data)
                synchronization(all_data[src])
            elif dst in all_data:
                all_data[dst].append(data)
                synchronization(all_data[dst])
        elif src in all_data:
            all_data[src].append(data)
        elif dst in all_data:
            all_data[dst].append(data)


if __name__ == '__main__':
    t = sniff(filter="port 9999", iface='\\Device\\NPF_Loopback', prn=simple_attack)
