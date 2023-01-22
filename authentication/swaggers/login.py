from drf_yasg import openapi

login_operation_description = '기능\n' \
                              '- 로그인\n' \
                              '- 현재 아이디/비밀번호 입력에 맞는 유저 id와 토큰 반환\n' \
                              '- 유저 id와 토큰만 반환하므로, 해당 정보를 바탕으로 유저 정보를 GET하는 요청을 보내주세요.\n' \
                              '\n권한\n' \
                              '- 관리자 계정\n' \
                              '- 로그인하지 않은 사용자\n' \
                              '\nrequest body\n' \
                              '- email(필수)\n' \
                              '- password(필수)\n' \
                              '\nresponses\n' \
                              '- 200: 로그인 완료\n' \
                              '- 400: 로그인 실패\n' \
                              '\n비고\n' \
                              '- 로그인을 통해 얻어온 access token은 Header에 key=Authorization, value=Bearer ${access_token}과 ' \
                              '같이 담아서 이후 요청에 보내주시면 됩니다.'

login_request_body = openapi.Schema(
    'Login',
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema('email', type=openapi.TYPE_STRING),
        'password': openapi.Schema('password', type=openapi.TYPE_STRING),
    },
    description='로그인을 위해 유저의 이메일과 비밀번호를 입력합니다.'
)

login_responses = {
    200: openapi.Schema(
        'Token',
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                default=True
            ),
            "token": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='유저의 토큰 정보를 담고 있는 오브젝트입니다.',
                properties={
                    'user_id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='현재 로그인한 사용자의 id(이메일 X)',
                    ),
                    'refresh_token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='jwt refresh token',
                    ),
                    'access_token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='jwt access token'
                    )
                }
            )
        }
    ),
    400: openapi.Schema(
        'Error',
        type=openapi.TYPE_OBJECT,
        properties={
            "non_field_erorrs": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='어쩌다보니 리스트를 반환하지만, 에러 메시지는 한 번에 하나만 반환됩니다. \n'
                            '아래 3개의 에러 메시지가 동시에 반환되는 경우는 없습니다!!',
                items=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='1. 입력한 이메일이 이메일 형식을 따르지 않을 때\n'
                                '- "Invalid email format" 반환\n'
                                '\n2. 입력한 이메일이 사용자 데이터베이스에 존재하지 않는 계정일 때\n'
                                '- "User does not exist" 반환\n'
                                '\n3. 입력한 이메일은 존재하는 계정이지만, 비밀번호가 틀렸을 때\n'
                                '- "Wrong password" 반환'
                )
            )
        }
    )
}

# login_responses = {
#     201: openapi.Schema(
#         'UserDetail',
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'id': openapi.Schema('user id', read_only=True, type=openapi.TYPE_INTEGER),
#             'email': openapi.Schema('email', type=openapi.TYPE_STRING),
#             'username': openapi.Schema('user name', type=openapi.TYPE_STRING),
#             'student_id': openapi.Schema('student_id', type=openapi.TYPE_STRING),
#             'is_professor': openapi.Schema('whether current user is professor', type=openapi.TYPE_BOOLEAN),
#             'is_superuser': openapi.Schema('whether current user is admin', type=openapi.TYPE_BOOLEAN),
#             'classes': openapi.Schema(
#                 type=openapi.TYPE_ARRAY,
#                 items=openapi.Schema(
#                     'Class',
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         'id': openapi.Schema('class id', read_only=True, type=openapi.TYPE_INTEGER),
#                         'name': openapi.Schema('class name', type=openapi.TYPE_STRING),
#                     }
#                 )
#             ),
#             'token': openapi.Schema('token', type=openapi.TYPE_STRING)
#         },
#         description='로그인한 유저의 정보를 반환합니다. 유저의 기본적인 정보(유저 id, 이름, 학번, 교수인지, 관리자인지)와 유저가 '
#                     '신청한 수업을 list에 담아 받을 수 있습니다. 유저의 token 또한 가져옵니다.'
#     ),
#     400: openapi.Schema(
#         'Error',
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'error': openapi.Schema(
#                 type=openapi.TYPE_STRING,
#                 default='email or password is not correct',
#             )
#         },
#         description='아이디 혹은 비밀번호 입력이 잘못되었을 때 발생하는 오류입니다.'
#     ),
# }
