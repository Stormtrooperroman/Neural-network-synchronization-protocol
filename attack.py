from scapy.all import *


all_data = {}


def simple_attack(pkt):
    data = pkt.sprintf("{Raw:%Raw.load%}")

    # print(pkt.sprintf("{IP:%IP.src%:%IP.dport% -> %IP.dst%:%IP.sport%\n}{Raw:%Raw.load%\n}"))

    if data and data != "":
        src = pkt.sprintf("{IP:%IP.src%:%IP.dport%}")
        dst = pkt.sprintf("{IP:%IP.dst%:%IP.sport%}")
        data = data[1:-3]
        # print(data)
        if data == "start synchronization":
            all_data[dst] = []

        if data == "finish synchronization":
            print("HAHAHAH")
        if src in all_data:
            all_data[src].append(f"{src} {dst} {data}")
        elif dst in all_data:
            all_data[dst].append(f"{src} {dst} {data}")


t = sniff(filter="port 9999", iface='\\Device\\NPF_Loopback', prn=simple_attack)

