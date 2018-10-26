#! /usr/bin/python3
#
# This program sets the IP packet loss ratio and counts the TCP retransmits
#
import ipaddress
import socket
import sys


def count_retries(source_addr: str, source_port: int, destination_addr: str,
                  destination_port: int, protocol: int) -> int:
    """
    This method returns the number of TCP retries for a given TCP connection

    :param source_addr:
    :param source_port:
    :param destination_addr:
    :param destination_port:
    :param protocol: one of two values: socket.AF_INET or socket.AF_INET6
    :return: count
    """

    def str_to_hex_addr(addr: str, protocol: int) -> str:
        """
        This converts an input string, such as 208.97.189.29 or
        2607:f298:5:115f::23:e397
        into a "exploded" string, such as
        :param addr: The address to be converted.
        :return: A string which is 8 characters long for IPv4 and 32
        characters long for IPv6 which
        is the IP address the way /proc/net/tcp returns it
        """

        add = ipaddress.ip_address(addr)
        if protocol == socket.AF_INET:
            add_exp: str = add.exploded
            add_hex = add_exp.replace(":", "")
            assert len(
                add_hex) == 32, f"IPv6 address should be 32 chars (16 bytes) " \
                                f"long {add_hex}"
        else:
            add_hex = "".join([f"{(int(i)):02x}" for i in str(add).split(".")])
            assert len(
                add_hex) == 8, f"IPv4 address should be 8 chars (4 bytes) " \
                               f"long {add_hex}"
        return add_hex

    assert (protocol == socket.AF_INET or protocol == socket.AF_INET6), \
        print(
            f"protocol is {protocol}, should be socket.AF_INET or "
            f"socket.AF_INET6",
            file=sys.stderr)

    source_addr_hex: str = str_to_hex_addr(source_addr)
    source_port_hex: str = f"{source_port:04x}"
    dest_addr_hex: str = str_to_hex_addr(destination_addr)
    dest_port_hex: str = f"{destination_port:04x}"
    source_str = source_addr_hex + ":" + source_port_hex
    dest_str = dest_addr_hex + ":" + dest_port_hex

    tcp_table_filename: str = (
        "/proc/sys/tcp" if protocol == socket.AF_INET else "/proc/sys/tcp6")
    with open(tcp_table_filename, "r") as t:
        connections = t.readlines()

    # Linear search to find our connection
    count = None
    for conn in connections:
        if "local_address" in conn:  # skip first line
            continue
        fields = conn.split()
        two_matches: bool = (fields[1] == source_str and fields[
            2] == dest_str) or \
                            (fields[2] == source_str and fields[1] == dest_str)
        source_addr_zero = ((protocol == socket.AF_INET) and (
                    source_addr_hex == "00000000")) or \
                           (
                                       source_addr_hex ==
                                       "00000000000000000000000000000000")
        source_port_zero = source_port_hex == "0000"
        one_match: bool = (source_addr_zero and source_port_zero and fields[
            2] == dest_str)
        if one_match or two_matches:
            count = int(fields[6])
            break
    return count


if "__main__" == __name__:
    remote_addr = sys.argv[1]
    remote_port = sys.argv[2]
    dest_tuple = (remote_addr, remote_port)
    # Starting in Python 3.2, create can use a specific source address/port pair
    s = socket.create_connection(dest_tuple, 1.5, [0, 0])
    src_addr, src_port = s.getsockname()
    dst_addr, dst_port = s.getpeername()
    c1 = count_retries(src_addr, src_port, dst_addr, dst_port, socket.AF_INET)
    data = b"sdfadfasdfqwerqwerwefsadfasdfasdfasdf"
    for i in range(100):
        s.send(data=data)
    c2 = count_retries(src_addr, src_port, dst_addr, dst_port,
                       socket.AF_INET)
    print(c2 - c1)
