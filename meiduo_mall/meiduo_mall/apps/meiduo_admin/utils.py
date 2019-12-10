
def jwt_response_payload_handler(token, user=None, resquest=None):
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }