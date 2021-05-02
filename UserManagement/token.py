from rest_framework_simplejwt.tokens import RefreshToken


def generateToken(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access':str(refresh.access_token),
        'refresh':str(refresh),
        'userName':str(user.username),
        'fullname':str(user.first_name)

    }

# def generateAccessToken(user):
#     access_token_payload = {
#         'user_id': str(user.id),
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
#         'iat': datetime.datetime.utcnow(),
#     }
#     access_token = jwt.encode(access_token_payload,
#                               settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
#     return access_token


# def generateRefreshToken(user):
#     refresh_token_payload = {
#         'user_id': str(user.id),
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
#         'iat': datetime.datetime.utcnow()
#     }
#     refresh_token = jwt.encode(
#         refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

#     return refresh_token