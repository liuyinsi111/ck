

import json
import base64
import hmac,hashlib

# token如何签发

# 头信息
header = {
  'typ': 'JWT',
  'alg': 'HS256'
}

# 把字典数据转化成字符串
header = json.dumps(header) # string
# 把json格式字符串经过base64编码得出token值的头部
header = base64.b64encode(header.encode()) # bytes
# header:  b'eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJIUzI1NiJ9'
print("header: ", header)


# 载荷
payload = {
    "user_id": 4,
    "age": 18,
    "name": "weiwei",
    "admin": True
}
payload = json.dumps(payload) # string
payload = base64.b64encode(payload.encode())
print("payload: ", payload)


# 签名(信息摘要)
# signature = ???
# 原数据 = header + '.' + payload
# 原数据 = "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJIUzI1NiJ9.eyJ1c2VyX2lkIjogNCwgImFnZSI6IDE4LCAiYWRtaW4iOiB0cnVlLCAibmFtZSI6ICJ3ZWl3ZWkifQ"
# 加盐哈希: secret_key参与哈希运算的密钥，绝对不能暴露
# signature = SHA256(原数据, secret_key)

# 1、构建哈希对象
SECRET_KEY = b'j*h(69kj^)ofyw+re!3!fpsh28a^wnm9iv1xv@9mi%^$)(dgm='
message = header + b'.' + payload
h_obj = hmac.new(SECRET_KEY, msg=message, digestmod=hashlib.sha256)
# 2、通过哈希对象，得出签名(信息摘要)
signature = h_obj.hexdigest()
print("signature: ", signature)


# token值
jwt_token = header.decode() + '.' + payload.decode() + '.' + signature
print("token值：", jwt_token)




# token如何验证

# 默认前端浏览器传递token值
# jwt_from_browser = jwt_token # 未篡改
jwt_from_browser = "abs" + jwt_token # 篡改

# 1、提取请求中的token中的header、payload和signature
header_from_browser = jwt_from_browser.split('.')[0]
payload_from_browser = jwt_from_browser.split('.')[1]
signature_from_browser = jwt_from_browser.split('.')[2]

# 2、把header和payload重新拼接得到待哈希的"原信息"
message_from_browser = header_from_browser + '.' + payload_from_browser

# 3、将"原信息"重新哈希运算(算法和密钥一定要和签发的时候一样)
h_obj = hmac.new(SECRET_KEY, msg=message_from_browser.encode(), digestmod=hashlib.sha256)
new_signature = h_obj.hexdigest()

# 4、对比新生成的签名，和前端传来的签名是否一致：是--未篡改；不是--篡改了！
if signature_from_browser == new_signature:
    print("数据完整！")
    user_info = json.loads(base64.b64decode(payload_from_browser.encode()).decode())
    print(user_info)
else:
    print("数据被篡改了！")




















