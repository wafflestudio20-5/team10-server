from drf_yasg import openapi

profile_put_operation_description = '기능\n' \
                                '- 로그인 한 User가 자신의 프로필 사진을 업로드합니다.\n' \
                                '\npermission\n' \
                                '- 로그인된 유저\n' \
                                '\nrequest body\n' \
                                '<Content-Type : multipart/form-data>\n' \
                                '- 이미지 파일\n' \
                                '\nresponse\n' \
                                '- 201: 업로드 성공'

profile_put_request_body = openapi.Schema(
    'File',
    type=openapi.TYPE_OBJECT,
    required=['file'],
    properties={
        'file' : openapi.Schema(type=openapi.TYPE_FILE),
    }
)
