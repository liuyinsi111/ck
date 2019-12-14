from django.contrib.auth.backends import ModelBackend
import re
from .models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
        return user
    except User.DoesNotExist:
        return None

class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user

def generate_email_verify_url(user):
    """
    生成邮箱激活url
    :param user: 那个用户要生成激活url
    :return: 邮箱激活url
    """
    # 创建加密实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    # 包装要加密的字典数据
    data = {'user_id': user.id, 'email': user.email}
    # loads方法加密
    token = serializer.dumps(data).decode()
    # 拼接激活url
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url


def get_user_token(token):
    """
    对token进行解密,并查询出对应的user
    :param token: 要解密的用户数据
    :return: user or None
    """
    # 创建解密实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    try:
        # 解密
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
            return user
        except User.DoesNotExist:
            return None


def jwt_response_payload_handler(token, user=None, resquest=None):
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }