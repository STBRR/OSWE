import sys

payload = input(str("Payload: "))

def enc_payload(payload):
    payload = payload.replace(' ', '+')
    payload = payload.replace('\'', '$$')
    payload = payload.replace('\\', '\\\\')
    print("[encoded]", payload)

def dec_payload(payload):
    payload = payload.replace('+', ' ')
    payload = payload.replace('$$', '\'')
    payload = payload.replace("\\\\", "\\")
    print("[decoded]", payload)


enc_payload(payload)
dec_payload(payload)
