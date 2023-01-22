from drf_yasg import openapi

post_comments_post_request_body = openapi.Schema(
    'Comment',
    type=openapi.TYPE_OBJECT,
    properties={
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='댓글 내용입니다.',
        ),
    }
)

# TODO: 서버 재배포 시 권한 문제 해결됨. 비고 수정.
post_comments_post_operation_description = '기능\n' \
                                           '- 특정 게시글에 댓글 생성\n' \
                                           '- {id}에는 게시글(공지사항, 질문글)의 id가 들어갑니다.\n' \
                                           '\npermission\n' \
                                           '- admin 계정\n' \
                                           '- 로그인하고, 개인정보 세팅을 완료한 사용자\n' \
                                           '\nrequest body\n' \
                                           '- content(필수)\n' \
                                           '\nresponses\n' \
                                           '- 201: 특정 게시글에 댓글 생성 성공\n' \
                                           '\n비고\n' \
                                           '- 동일한 URL로 특정 게시글의 댓글 리스트를 불러오는 GET 요청은 만들지 않았습니다.\n' \
                                           '이는 etl/announcement/{id}/ 또는 etl/question/{id}/ 에 GET 요청을 넣을 때 해당 id를 가진 게시글의 댓글 리스트를 반환해주기 때문입니다.\n' \
                                           '만약 페이지네이션을 고려한다면 동일한 URL로 GET 요청을 구현할 필요가 있으나, 당장은 고려에 넣지 않았습니다.\n' \
                                           '댓글에도 페이지네이션 기능이 필요하다고 생각하시면, 말씀 부탁드립니다.\n' \
                                           '- 현재 권한 설정을 잘못 했습니다. 지금은 admin 계정 혹은 교수 계정 혹은 해당 게시글을 생성한 사람만 댓글을 달 수 있습니다. 다음에 서버에 배포할 때 해결하겠습니다.'

post_comments_post_responses = {
    201: openapi.Schema(
        'Comment',
        type=openapi.TYPE_OBJECT,
        description='방금 생성된 댓글 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='댓글 내용입니다.',
            ),
            'created_by': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='해당 댓글을 생성한 사람의 정보입니다.',
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        read_only=True,
                    ),
                    'username': openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    'student_id': openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                    'is_professor': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='유저가 교수인지, 학생인지 정보를 반환합니다.'
                    ),
                },
            ),
            'created_at': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='timestamp 형식으로 게시글 생성 시간을 반환합니다.'
            ),
        }
    )
}
