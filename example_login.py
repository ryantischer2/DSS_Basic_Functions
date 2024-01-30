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

"""
The following is used for secure password storage.  Uncomment to use.

keyring should work on modern OS.  Only tested on MAC 13.  Visit the following to make it work in your OS
https://pypi.org/project/keyring/

Must run init program first.
"""

"""
import keyring

creds =  (keyring.get_credential("pensando", "admin"))

with open('pypen_init_data.json') as json_file:
    jdata = json.load(json_file)
    PSM_IP = jdata["ip"]
    PSM_TENANT = jdata["tenant"]
    PSM_USERNAME = creds.username
    PSM_PASSWD = creds.password
#end secure environment vars
"""

#static PSM vars.  Uncomment to use


#input PSM Creds
PSM_IP = 'https://10.9.9.70'
username = 'admin'
password = 'Pensando0$'

#Create auth session

try:
    session = pen_auth.psm_login(PSM_IP, username, password)

except Exception as e:
            message = f"An error occurred: {str(e)}"

except requests.exceptions.Timeout:
        print('Network Timeout')

except requests.exceptions.TooManyRedirects:
        print('too Many Redirects')

except requests.exceptions.RequestException as err:
        print('Something went wrong')

#pass session to get data
NSP = pen.get_networksecuritypolicy(PSM_IP, session)

#parse json response

policyID = []

for i in range(len(NSP['items'])):
    print (NSP['items'][i]['meta']['display-name'])
    policyID.append(NSP['items'][i]['meta']['name'])

#psm policy is reference by a uuid name.  In this case stored in a list called policyID
singlePolicy = pen.get_Specificpolicy(PSM_IP, session, policyID[1])

print (json.dumps(singlePolicy, indent=2))
