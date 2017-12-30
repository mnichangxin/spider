import requests
import json
import time
from Crypto.Cipher import AES
import base64

action_data = {
    "score": 1024,
    "times": 666,
    "game_data": "{}"
}

session_id = "9SuzouVoiIG8PyF3KOthtGFimAt1jsTYLsWfiVSCFGRT2lxAa8okjz/Vx6dZMk+GN+LLHAOeEltL4LRVGi0ZGrfCqa3n4n1O9cUMcTKYknhB+yLGE8tD93T0273TrOgkyA8tsv/Ov44rVqW9M1AqIg=="

aes_key = session_id[0:16]
aes_iv  = aes_key

cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)

str_action_data = json.dumps(action_data).encode("utf-8")
print("json_str_action_data ", str_action_data)

#Pkcs7
length = 16 - (len(str_action_data) % 16)
str_action_data += chr(length)*length
cipher_action_data = base64.b64encode(cryptor.encrypt(str_action_data)).decode("utf-8")
print("action_data ", cipher_action_data)

post_data = {
  "base_req": {
    "session_id": session_id,
    "fast": 1,
  },
  "action_data": cipher_action_data
}

headers = {
    "charset": "utf-8",
    "Accept-Encoding": "gzip",
    "referer": "https://servicewechat.com/wx7c8d593b2c3a7703/3/page-frame.html",
    "content-type": "application/json",
    "User-Agent": "MicroMessenger/6.6.1.1200(0x26060130) NetType/WIFI Language/zh_CN",
    "Content-Length": "0",
    "Host": "mp.weixin.qq.com",
    "Connection": "Keep-Alive"
}

url = "https://mp.weixin.qq.com/wxagame/wxagame_settlement"


response = requests.post(url, json=post_data, headers=headers, verify=False)
print(json.loads(response.text))