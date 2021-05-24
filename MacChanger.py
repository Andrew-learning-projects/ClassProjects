#!/usr/bin/env python

import subprocess
# lets us run commands
import optparse
# lets us add cmd parsing/options
import re
# imports regex stuff


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] please specify an interface")
    # checks for no option to return error
    elif not options.new_mac:
        parser.error("[+] please specify a MAC address")
        # another error check
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    # prints statement in cmd interface

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    # These take down the interface and re-up it with new mac address
    # the listed way makes all strings+Vars part of the same command
    # this way prevents unauthorized command executions


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[+] could not find MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current Mac = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[+] MAC address was not changed")
