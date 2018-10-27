#! /usr/bin/python3
#
# This program sets the IP packet loss ratio and counts the TCP retransmits
#
import ipaddress
import socket
import sys
from typing import Tuple


def count_retries(source_addr: str, source_port: int, destination_addr: str,
                  destination_port: int, lcl_protocol: int) -> int:
    """
    This method returns the number of TCP retries for a given TCP connection

    :param source_addr:
    :param source_port:
    :param destination_addr:
    :param destination_port:
    :param lcl_protocol: one of two values: socket.AF_INET or socket.AF_INET6
    :return: count
    """

    def str_to_hex_addr(addr: str, s2ha_protocol: int) -> str:
        """
        This converts an input string, such as 208.97.189.29 or
        2607:f298:5:115f::23:e397
        into a "exploded" string, such as
        :param addr: The address to be converted.
        :param s2ha_protocol: either socket.AF_INET or socket.AF_INET6
        :return: A string which is 8 characters long for IPv4 and 32
        characters long for IPv6 which
        is the IP address the way /proc/net/tcp returns it
        """
        add = ipaddress.ip_address(addr)
        if s2ha_protocol == socket.AF_INET6:
            add_exp: str = add.exploded
            add_hex = add_exp.replace(":", "")
            assert len(add_hex) == 32, \
                f"IPv6 address should be 32 chars (16 bytes) long {add_hex}"
        else:
            add_hex = "".join([f"{(int(i2)):02x}" for i2 in str(add).split(".")])
            assert len(add_hex) == 8, f"IPv4 address should be 8 chars " \
                                      f"(4 bytes) long {add_hex}"
        return add_hex

    assert (lcl_protocol == socket.AF_INET or lcl_protocol == socket.AF_INET6), \
        print(
            f"lcl_protocol is {lcl_protocol}, should be socket.AF_INET or "
            f"socket.AF_INET6",
            file=sys.stderr)

    source_addr_hex: str = str_to_hex_addr(source_addr, s2ha_protocol=lcl_protocol).upper()
    # I came across a case where the source address was 192.168.0.21 and the
    # source_addr_hex was c0a80015, which is correct.  However, the address in
    # the table from /proc/net/tcp was 1500A8C0
    source_port_hex: str = f"{source_port:04x}".upper()
    dest_addr_hex: str = str_to_hex_addr(destination_addr, s2ha_protocol=lcl_protocol).upper()
    dest_port_hex: str = f"{destination_port:04x}".upper()
    source_str = (source_addr_hex + ":" + source_port_hex).upper()
    dest_str = (dest_addr_hex + ":" + dest_port_hex).upper()

    tcp_table_filename: str = (
        "/proc/net/tcp" if lcl_protocol == socket.AF_INET else "/proc/net/tcp6")
    with open(tcp_table_filename, "r") as t:
        connections = t.readlines()

    # Linear search to find our connection
    # The documentation on the contents of /proc/net/tcp is at
    # http://lkml.iu.edu/hypermail/linux/kernel/0409.1/2166.html
    # See also https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.txt
    for conn in connections:
        if "local_address" in conn:  # skip first line
            continue
        fields = conn.split()
        conn_src_addr_hex, conn_src_port_hex = fields[1].split(":")  # local address, since this is a client, the source
        conn_dst_addr_hex, conn_dst_port_hex = fields[2].split(":")  # remote address, the destination
        conn_src_port = int(conn_src_port_hex, 16)
        conn_dst_port = int(conn_dst_port_hex, 16)
        two_matches: bool = (fields[1] == source_str and fields[2] == dest_str)
        source_addr_zero = ((lcl_protocol == socket.AF_INET) and (
                source_addr_hex == "00000000")) or (
                                   "00000000000000000000000000000000" == source_addr_hex)
        source_port_zero = source_port_hex == "0000"
        one_match: bool = (source_addr_zero and source_port_zero and fields[
            2] == dest_str)
        # This is the weakest comparison, most likely for a true match, also most
        # likely for a false match. If I can get the other two camparisons to work
        # then this should go away.
        # The assert is here because I actually had this issue come up.
        assert type(conn_src_port) == type(source_port) and \
            type(conn_dst_port) == type(destination_port)
        port_match: bool = (conn_src_port == source_port) and (conn_dst_port == destination_port)
        if port_match and not (one_match or two_matches):
            print("Port match fired but neither of the other two matches "
                  f"fired.  Why?\n  src_port={conn_src_port} "
                  f"source_port={source_port} dst_port={conn_dst_port} "
                  f"destination_port={destination_port}\n" +
                  connections[0], "\n", conn, "\n", file=sys.stderr)
        if one_match or two_matches or port_match:
            count = int(fields[6])
            break
    else:
        raise AssertionError(
            f"The connection was not found in the TCP connection table.  " +
            f"dest_str={dest_str}, source_str={source_str}" +
            "\n".join(connections))

    return count


if "__main__" == __name__:
    if len(sys.argv) > 2:
        remote_addr = sys.argv[1]
        remote_port = sys.argv[2]
        protocol_str = sys.argv[3] if len(sys.argv) > 3 else "-4"
    else:
        remote_addr = "commercialventvac.com"  # "2607:f298:5:115f::23:e397"
        remote_port = "4000"
        protocol_str = "-6"
    protocol: socket.AddressFamily = (socket.AF_INET6 if protocol_str == "-6" else socket.AF_INET)
    if protocol == socket.AF_INET:
        dest_tuple: Tuple[str, int] = (remote_addr, int(remote_port))
    else:
        # The extra information is flowinfo and  scopeid.  See
        # https://docs.python.org/3/library/socket.html#socket-families
        dest_tuple: Tuple[str, int, int, int] = (remote_addr, int(remote_port), 0, 0)
    # Starting in Python 3.2, create can use a specific source address/port pair
    # Not sure how to tell which protocol was selected
    # s = socket.create_connection(dest_tuple, 1.5, ("0", 0))
    s = socket.socket(family=protocol, type=socket.SOCK_STREAM)
    assert s.family == protocol, "socket.create_connection used the wrong protocol" \
                                 f"Should have been {protocol} was actually {s.family}"
    try:
        s.connect(dest_tuple)
    except ConnectionRefusedError as c:
        print(f"The socket connect call failed to connect to {dest_tuple}.  "
              f"Try running nc -k -l {remote_port} on {remote_addr} \n{str(c)}\n",
              file=sys.stderr)
        raise
    try:
        if s.family == socket.AF_INET:
            nom_src_addr, nom_src_port = s.getsockname()
            nom_dst_addr, nom_dst_port = s.getpeername()
        else:
            nom_src_addr, nom_src_port, flowinfo_s, scopeid_s = s.getsockname()
            nom_dst_addr, nom_dst_port, flowinfo_d, scopeid_d = s.getpeername()
        try:
            c1: int = count_retries(nom_src_addr, nom_src_port, nom_dst_addr,
                                    nom_dst_port, lcl_protocol=protocol)
        except AssertionError as a:
            print("Caught AssertionError from count_retries", file=sys.stderr)
            c1 = 0
        data = b"sdfadfasdfqwerqwerwefsadfasdfasdfasdf"
        for i in range(100):
            s.send(data)
        try:
            c2: int = count_retries(nom_src_addr, nom_src_port, nom_dst_addr,
                                    nom_dst_port, lcl_protocol=protocol)
        except AssertionError as a:
            print("Caught AssertionError from count_retries", file=sys.stderr)
            c2 = 0
        print(c2 - c1)
    except FloatingPointError as e:
        print("Something went wrong somewhere " + str(e))
    s.close()
