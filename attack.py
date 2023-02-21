from scapy.all import *
import IPython


def simple_attack(pkt):
    print(pkt.sprintf("{Raw:%Raw.load%\n}"))


conf.L3socket
t = sniff(filter="port 9999", iface='\\Device\\NPF_Loopback', prn=simple_attack)

