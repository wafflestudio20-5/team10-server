from drf_yasg import openapi

assignments_get_operation_description = '기능\n' \
                                        '- 모든 Assignment List를 반환합니다.\n' \
                                        '- 현재 유저가 듣는 수업과 상관없이, 모든 Assignment list를 반환합니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200: assignment list'

assignments_post_operation_description = '기능\n' \
                                        '- Assignment를 생성합니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 교수\n' \
                                        '\nrequest body\n' \
                                        '<Content-Type : multipart/form-data>\n' \
                                        '- 수업 id\n' \
                                        '- 과제 이름\n' \
                                        '- 마감 기한\n' \
                                        '- 최대 점수\n' \
                                        '- 가중치(0과 1사이의 실수)\n' \
                                        '- 과제 파일(선택)\n'    \
                                        '\nresponse\n' \
                                        '- 201: assignment 생성'

assignments_post_request_body = openapi.Schema(
    'Assignment',
    type=openapi.TYPE_OBJECT,
    required=['lecture', 'name', 'due_date', 'max_grade', 'weight'],
    properties={
        'lecture': openapi.Schema(type=openapi.TYPE_INTEGER),
        'name': openapi.Schema(type=openapi.TYPE_STRING),
        'due_date': openapi.Schema(type=openapi.FORMAT_DATETIME),
        'max_grade': openapi.Schema(type=openapi.FORMAT_DOUBLE),
        'weight': openapi.Schema(type=openapi.FORMAT_DOUBLE),
        'file': openapi.Schema(type=openapi.TYPE_FILE)
    }
)
