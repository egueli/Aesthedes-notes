#!/usr/bin/env python3

import socket
import time
import sys

# Entry IDs with "(no action)" description
ENTRY_IDS = [
    4, 5, 8, 11, 14, 15, 19, 21, 22, 23, 36, 37, 40, 68, 69, 72, 76, 78, 85, 86,
    100, 104, 118, 199, 210, 212, 215, 268, 274, 276, 279, 359, 370, 373, 516, 518,
    519, 520, 521, 522, 553, 554, 555, 558, 561, 625, 626, 648, 649, 651, 652, 653,
    660, 690, 694, 708, 709, 714, 726, 746, 757, 779, 789, 1028, 1031, 1039, 1128,
    1129, 1256, 1352, 1357, 1358, 1382, 1383, 1418, 1421, 1422, 1484, 1486, 1545, 1546,
    1547, 1548, 1549, 1558, 1573, 1574, 1575, 1590, 1604, 1606, 1804, 1808, 1809, 1810,
    1836, 1840, 1841, 1842, 1868, 1872, 1873, 1874, 1900, 1904, 1905, 1906, 1932, 1936,
    1937, 1938, 1964, 1968, 1969, 1970, 2004, 2005, 2006, 2007, 2038, 2092, 2096, 2097,
    2098, 2100, 2101, 2103, 2128, 2132, 2135, 2156, 2160, 2161, 2162, 2167, 2183, 2214,
    2215, 2218, 2219, 2220, 2221, 2222, 2251, 2252, 2253, 2256, 2278, 2315, 2316, 2317,
    2320, 2342, 2375, 2384, 2438, 2439, 2440, 2441, 2442, 2443, 2445, 2446, 2447, 2448,
    2449
]

def read_until_ok(sock):
    """Read from socket until 'OK' is received"""
    data = b''
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
        if b'OK' in data:
            break
    return data

def main():
    try:
        # Connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 6822))
        print(f"Connected to 127.0.0.1:6822")
        
        for i, entry_id in enumerate(ENTRY_IDS):
            print(f"\n[{i+1}/{len(ENTRY_IDS)}] Testing entry ID: {entry_id}")
            
            print(f"  Sending: 1354 (From Disk)")
            sock.sendall(b'1354\n')
            read_until_ok(sock)

            print(f"  Waiting 1 second...")
            time.sleep(1)

            print(f"  Sending: {entry_id}")
            sock.sendall(f'{entry_id}\n'.encode())
            read_until_ok(sock)
            
            print(f"  Waiting 2 seconds...")
            time.sleep(2)

            print(f"  Sending: 523 (ESC / Abort)")
            sock.sendall(b'523\n')
            read_until_ok(sock)
            
            print(f"  Waiting 1 second...")
            time.sleep(1)

        
        sock.close()
        print(f"\nCompleted testing all {len(ENTRY_IDS)} entry IDs")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
