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

#get apps and IP collections from PSM
apps = pen.get_psm_apps(PSM_IP, session)
ipcollect = pen.get_psm_ipcollections(PSM_IP, session)


#Build reference table of apps/ipcollections UUID to display name

appsRef = {}

for data in apps["items"]:
   
    #sometimes [meta][name] is the UUID, other times not
    tempName = data["meta"]["name"]
    uuid = data["meta"]["uuid"]
    
    if len(tempName) == 36: #UUID is 36 chars
        displayName = data["meta"]["display-name"]
    else:
        displayName = data["meta"]["name"]

    appsRef[uuid] = displayName

ipcollectRef = {}

for data in ipcollect["items"]:

    tempName = data["meta"]["name"]
    uuid = data["meta"]["uuid"]
   
    if len(tempName) == 36: #UUID is 36 chars
        displayName = data["meta"]["display-name"]
    else:
        displayName = data["meta"]["name"]


    ipcollectRef[uuid] = displayName

policy = {}
#push policy to psm

#first parse the json and look for UUID
#todo

for data in policy["spec"]["rules"]:
     if data["apps"]:
          


#replace uuid with name    
def f_r_ipcollect(key):

    return ipcollectRef.get(key, "Key not found")

def f_r_apps(key):

    return appsRef.get(key, "Key not found")
