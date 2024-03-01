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

import pen, pen_auth, json

#NOTE - Object renaming should be disabled when using the API

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

#open apps file scrub and save
def scrub_apps():
    
    #PSM requires apps be created one at a time.  This function returns a list of valid json to send to PSM
     #get the current apps
    
    apps_data = pen.get_psm_apps(PSM_IP, session)

    numItems = len(apps_data["items"])
    return_list = []
   
    for i in range(numItems):

        if len(apps_data["items"][i]["meta"]["name"]) == 36:
            tempName = "display-name"
        else:
            tempName = "name"

        scrub_data = {
            "meta": {
            "name": apps_data["items"][i]["meta"][tempName],
            "tenant": "default"
                    },
            "spec": {
            "proto-ports": apps_data["items"][i]["spec"]["proto-ports"]
                    }
                    }
        
        return_list.append(json.dumps(scrub_data))

    return return_list

#open ip collections scrub and save
def scrub_ipcollections():
    
    #PSM requires ipcollections be created one at a time.  This function returns a list of valid json to send to PSM
     #get the current apps
    
    apps_data = pen.get_psm_ipcollections(PSM_IP, session)

    numItems = len(apps_data["items"])
    return_list = []
   
    for i in range(numItems):

        if len(apps_data["items"][i]["meta"]["name"]) == 36:
            tempName = "display-name"
        else:
            tempName = "name"

        scrub_data = {
            "meta": {
            "name": apps_data["items"][i]["meta"][tempName]
                    },
                    "spec": {"addresses": apps_data["items"][i]["spec"]["addresses"]
                    }}
        return_list.append(json.dumps(scrub_data))

    return return_list
    

scrubedApps =  scrub_apps()
scrubedIPcollect = scrub_ipcollections()

#example push to PSM#
#may need to build new session to new PSM

#input PSM Creds

PSM_IP = 'https://10.9.9.104'
username = 'admin'
password = 'Pensando0$'

#Create auth session

session = pen_auth.psm_login(PSM_IP, username, password)

#if login does not work exit the program
if session is None:
    print ("Login Failed")
    exit()


#push apps and IP collections to the new PSM.   delay inserted to limited api calls to PSM
import time

#first example checks status codes

for item in scrubedApps:
    return_code = pen.create_apps(PSM_IP, session, json.loads(item))
    print (return_code)
    #optional check status codes
    if str(return_code) == "<Response [200]>":   # does not work yet
        print (f"{item} was successfully installed")

    time.sleep(1)

print ("done with apps")
for item in scrubedIPcollect:
    pen.create_ipcollections(PSM_IP, session, json.loads(item))
    time.sleep(1)
