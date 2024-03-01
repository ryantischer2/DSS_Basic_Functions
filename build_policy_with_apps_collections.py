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


#2 functions find/replace uuid with name    
def f_r_ipcollect(key, data):

    tempList = []
    tempList.append(data.get(key))
    return tempList

def f_r_apps(key):

    return appsRef.get(key, "Key not found")

###########################push policy to psm

#get the policy

# The path to your JSON file
file_path = 'zeroTrustPolicyFromPSM.json'

with open(file_path, 'r') as file:
    policy = json.load(file)

numRules = len(policy["spec"]["rules"])

#iterate over the policy and swap uuid for name.  Have to check each key make better later

for i in range(numRules):

    #change IP collections 
    if "from-ipcollections" in policy["spec"]["rules"][i]:
         
        numItems = len(policy["spec"]["rules"][i]["from-ipcollections"])

        for ia in range(numItems):
            #get uuid to name map
            tempUUID = policy["spec"]["rules"][i]["from-ipcollections"][ia]
    
            policy["spec"]["rules"][i]["from-ipcollections"] = f_r_ipcollect(tempUUID, ipcollectRef)


    #change IP collections 
    if "to-ipcollections" in policy["spec"]["rules"][i]:
         
        numItems = len(policy["spec"]["rules"][i]["to-ipcollections"])

        for ia in range(numItems):
            #get uuid to name map
            tempUUID = policy["spec"]["rules"][i]["to-ipcollections"][ia]
    
            policy["spec"]["rules"][i]["to-ipcollections"] = f_r_ipcollect(tempUUID, ipcollectRef)

     #change apps 
    if "apps" in policy["spec"]["rules"][i]:
         
        numItems = len(policy["spec"]["rules"][i]["apps"])

        for ia in range(numItems):
            #get uuid to name map
            tempUUID = policy["spec"]["rules"][i]["apps"][ia]
    
            policy["spec"]["rules"][i]["apps"] = f_r_ipcollect(tempUUID, appsRef)

#format dict to remove keys

keys_to_keep = {"kind", "api-version", "tenant", "meta", "spec"}

# Iterate over a list of the dictionary's keys and remove those not in `keys_to_keep`
for key in list(policy.keys()): 
    if key not in keys_to_keep:
        del policy[key]
    if key == "meta":
        keys_to_keep_meta = {"display-name", "tenant"}
        for key2 in list(policy["meta"].keys()):
            if key2 not in keys_to_keep:
                del policy["meta"][key2]

#print (json.dumps(policy))
pen.create_psm_policy(PSM_IP, session, policy)
