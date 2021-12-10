#!/usr/bin/env python

import scapy.all as scapy
import optparse


def get_iparg():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip", dest="ip", help="define which ip address or range to scan")
    (options, arguments) = parser.parse_args()
    return options
# allows input from user to put in ip address or ip range

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
# sets MAC address as broadcast for ARP request
    arp_request_broadcast = broadcast/arp_request
# combines both objects into the packet for the arp request on the broadcast address
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
# displays the answered arp requests and times out if it takes too long
    client_list = []
    for element in answered_list:
        client_dictionary = {"IP": element[1].psrc, "MAC Address": element[1].hwsrc}
        client_list.append(client_dictionary)
    return client_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n------------------------------------------------")
    for client in results_list:
        print(client["IP"] + "\t\t" + client["MAC Address"])

# parses the request to display relevant ip and MAC addresses from answered requests

options = get_iparg()
# calls back to user input to add ip address to scan
scan_options = get_iparg()
scan_result = scan(scan_options.ip)
print_result(scan_result)

