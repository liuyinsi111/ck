# import json
# import base64
# import hmac,hashlib
#
# header = {
#     'typ':'JWT',
#     'alg':'HS256'
# }
# header = json.dumps(header)
# header = base64.b64encode(header.encode())
#
# payload = {
#     'user_id': 1,
#     'age': 18,
#     'name': '111111aq',
#     'admin': True
# }
#
# payload = json.dumps(payload)
# payload = base64.b64encode(payload.encode())
#
#
# SECRET_KEY = b'0^wo+z5&5zx1)3y+5w#+0n6z1a3d4*2qg1&ig$31xfboitlb!*'
# message = header + b'.'+ payload
# h_obj = hmac.new(SECRET_KEY, msg=message, digestmod=hashlib.sha256)
# signature = h_obj.hexdigest()
#
# jwt_token = header.decode()+'.'+payload.decode()+'.'+signature
# jwt_from_browser = 'abs'+jwt_token
# header_from_browser = jwt_from_browser.split('.')[0]
# payload_from_browser = jwt_from_browser.split('.')[1]
# signature_from_browser = jwt_from_browser.split('.')[2]
#
# message_from_browser = header_from_browser+'.'+payload_from_browser
# h_obj = hmac.new(SECRET_KEY, msg=message_from_browser.encode(),
#                  digestmod=hashlib.sha256)
# new_signature = h_obj.hexdigest()
# if signature_from_browser == new_signature:
#     print('数据完整!')
#     user_info = json.loads(base64.b64decode(payload_from_browser.encode()).decode())
#     print(user_info)
# else:
#     print('数据被篡改了！')