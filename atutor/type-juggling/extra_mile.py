import hashlib
import re

account_id = 1
g_time = 19555
password_hash = "8635fc4e2a0c7d9d2d9ee40ea8bf2edd76d5757e"

hash_digits = int(re.findall('^\d+', password_hash)[0])


found = False

while(not found):
    ready_to_hash = int(account_id + g_time + hash_digits)
    hashed = hashlib.sha1(str(ready_to_hash).encode()).hexdigest()[5:20]

    if re.match(r'0+[eE]\d+$', hashed):
        print(f"!!!!! {g_time} - {hashed}")
        break
    else:
        g_time += 1

