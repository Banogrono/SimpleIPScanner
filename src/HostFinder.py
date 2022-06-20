#!/usr/bin/env python3.8
import os
import socket
import subprocess


# todo: think about refactoring this file


# tcp ports used by Linux, Windows and MacOS
# ports = [20, 21, 22, 23, 25, 80, 111, 135, 137, 138, 139, 443, 445, 548, 631, 631, 993, 995]

# ---------------------------------------------------------------------------------------------------------
# Methods
# ---------------------------------------------------------------------------------------------------------

def find_hosts_by_scanning_ports(ip_lower_boundary=10, ip_upper_boundary=40, *args):
    print("TCP start")

    ports = args

    # note to self: lists act like reference types in Java, ergo list in this function is passed by reference.
    # (https://stackoverflow.com/questions/53459338/is-list-pass-by-value-or-by-reference)
    addr_list = generate_ip_addresses_in_range(ip_lower_boundary, ip_upper_boundary)

    online_list = []

    for addr in addr_list:
        for port in ports:
            result = check_host(addr, port)
            if result is not None:
                online_list.append(result)

    return online_list


def print_out_found_hosts(online_list):
    print(f"\nHosts found:")
    for host in online_list:
        print("Online:", host)


def check_host(addr, port):
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(0.5)
        result = test_socket.connect_ex((addr, port))
        if result == 0:
            test_socket.close()
            # if host is found, return a tuple with IP address and open port
            return addr
    except socket.error:
        print(socket.error)
        return None
    return None


def generate_ip_addresses_in_range(ip_lower_boundary, ip_upper_boundary):
    addresses = []
    for i in range(ip_lower_boundary, ip_upper_boundary):
        addresses.append('192.168.1.' + str(i))
    return addresses


def find_hosts_by_pinging(ip_lower_boundary=10, ip_upper_boundary=40):
    print("ping start")
    addresses = generate_ip_addresses_in_range(ip_lower_boundary, ip_upper_boundary)
    active_hosts = []

    for address in addresses:
        # todo: there's gotta be a better way than calling subprocess
        res = subprocess.call(["ping", address, "-c1", "-W2", "-q"], stdout=open(os.devnull, 'w'))
        if res == 0:
            active_hosts.append(address)

    return active_hosts


def get_device_name(list_of_hosts):
    for host in list_of_hosts:
        try:
            result = dns.resolver.resolve(host, 'PTR')
            print(result)
        except Exception:
            print("Something gone wrong for:", host)
