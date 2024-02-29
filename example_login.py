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
from terminaltables import AsciiTable

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

#pass session to get data
NSP = pen.get_networksecuritypolicy(PSM_IP, session)

#parse json response

policyID = []
policyNamepair = [['Policy Name', 'UUID', 'Prop Status', 'Num Rules', 'Last modified' ]]

for i in range(len(NSP['items'])):
    
    print (NSP['items'][i]['meta']['display-name'])

    #since were here store the policy uuid to reference later in pen.get_singlepolicy
    policyID.append(NSP['items'][i]['meta']['name'])

    #might be helpful to replace build a list of interesting data
    numRules = len(NSP['items'][i]['spec']['rules'])

    tempPair = [NSP['items'][i]['meta']['display-name'],
                NSP['items'][i]['meta']['name'], 
                NSP['items'][i]['status']['propagation-status']['status'], 
                numRules,
                NSP['items'][i]['meta']['mod-time']]
    
    policyNamepair.append(tempPair)


#other pen examples.  NOTE:   pass 'pretty=True' for data formating
    
#get psm cluster infomation
print (pen.get_psm_cluster(PSM_IP, session, pretty=True))

#get redirected networks
print (pen.get_networks(PSM_IP, session, pretty=True))

#get DSS
print (pen.get_dss(PSM_IP, session, pretty=True))

#psm policy is reference by a uuid name.  In this case stored in a list called policyID
#use json dumps directly instead of pretty=True
singlePolicy = pen.get_Specificpolicy(PSM_IP, session, policyID[1])
print (json.dumps(singlePolicy, indent=2))

#print policy display name and UUID
table = AsciiTable(policyNamepair)
table.justify = 'center'
table.inner_row_border = True
print(table.table)

