#!/usr/bin/python3

import base64
from subprocess import run, PIPE

while 1:
    try:
        decoded_bytes = base64.b64decode(input("Insert string: "))[5:]
        process = run(['protoc', '--decode_raw'], stdout=PIPE, input=decoded_bytes)

        print("\n\033[94mResult:\033[0m")
        print (str(process.stdout.decode("utf-8").strip()))
    except KeyboardInterrupt:
        break
