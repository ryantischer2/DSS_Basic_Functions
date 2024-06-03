# Copyright (c) 2024, AMD
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# Author: Ryan Tischer ryan.tischer@amd.com


import sys, json

#example use - "python netgen.py 10,11,150-200"

def process_input(user_input):

    numbers = set()
    parts = user_input.split(',')

    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start > end:
                print(f"Invalid range: {part}")
                continue
            numbers.update(range(start, end + 1))
        else:
            numbers.add(int(part))

    return sorted(numbers)

def create_json(vlan):

    tempDict = {
        "name": "network" + str(vlan),
        "vlan-id": str(vlan),
        "virtual-router": "default",
        "ingress-security-policy": [],
        "egress-security-policy": [],
        "maximum-cps": 0,
        "maximum-sessions": 0,
        "connection-tracking-mode": "inherit_from_vrf",
        "service-bypass": "false" # toggle to true
                }

    return tempDict

def write_to_json_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input>")
        sys.exit(1)

    user_input = sys.argv[1]
    networks = process_input(user_input)
    print("Processed numbers:", networks)

    #create json
    finalData = []
   
    for vlan in networks:
        tj = create_json(vlan)
        finalData.append(tj)

        
    #wite out file
    write_to_json_file(finalData, "networks.json")
    print("Data has been written to networks.json")