# Copyright (c) 2024, Pensando Systems
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




import pen, pen_auth

#input PSM Creds
PSM_IP = 'https://10.9.9.9'
username = 'admin'
password = 'Pensando0$'

#Create auth session
session = pen_auth.psm_login(PSM_IP, username, password)

#pass session to get data
NSP = pen.get_networksecuritypolicy(PSM_IP, session)

print (NSP['items'][0]['meta']['display-name'])