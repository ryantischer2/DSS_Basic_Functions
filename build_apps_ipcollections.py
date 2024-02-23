# Copyright (c) 2024, AmD
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

import pen, pen_auth, json, requests
from terminaltables import AsciiTable

"""
The following is used for secure password storage.  Uncomment to use.

keyring should work on modern OS.  Only tested on MAC.  Visit the following to make it work in your OS
https://pypi.org/project/keyring/

Must run init program first.
"""
'''
import keyring

creds =  (keyring.get_credential("pensando", "admin"))

with open('pypen_init_data.json') as json_file:
    jdata = json.load(json_file)
    PSM_IP = jdata["ip"]
    username = creds.username
    password = creds.password
#end secure environment vars
'''
#static PSM vars.  Uncomment to use

#input PSM Creds

PSM_IP = 'https://10.9.9.70'
username = 'admin'
password = 'Pensando0$'

#Create auth session

session = pen_auth.psm_login(PSM_IP, username, password)

#if login does not work exit the program
if session is None:
    print ("Login Failed")
    exit()

app_data = {
    "meta": {
    "Name": "emailservice2",
    "tenant": "default"
    },
    "spec": {
      "proto-ports": [
        {
          "protocol": "tcp",
          "ports": "5000,8080"
        }
      ]
    }}

ipc_data = {
  "meta": {
    "name": "ip_collection_test_fabric"
  },
  "spec": {
    "addresses": [
      "10.0.0.0/24",
      "1.1.1.1/32"
    ]
  }
}

print (pen.create_apps(PSM_IP, session, app_data))

print (pen.create_ipcollections(PSM_IP, session, ipc_data))