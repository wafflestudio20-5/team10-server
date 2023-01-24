from drf_yasg import openapi

# TODO: 댓글 수 기능 정상 구현 후 swagger 수정
class_announcements_get_operation_description = '기능\n' \
                                               '- 특정 수업에 해당하는 모든 공지사항 목록을 가져옵니다.\n' \
                                                '- {id}에는 class id가 들어갑니다.\n' \
                                                '- 페이지네이션이 적용되어 있습니다. 한 번에 공지사항 10개씩, 최근 순으로 가져옵니다.\n' \
                                                '\npermission\n' \
                                                '- admin 계정\n' \
                                                '- 로그인하고, 개인정보가 모두 세팅된 사용자\n' \
                                                '\nrequest body\n' \
                                                '- 아무것도 없습니다.\n' \
                                                '\nresponses\n' \
                                                '- 200: {id}에 해당하는 수업의 공지사항 목록 가져오기 성공\n' \
                                                '\n비고\n' \
                                                '- 공지사항에 달린 댓글에 갯수를 나타내는 "comment_count"가 response에 ' \
                                                '추가되었지만, 아직 기능이 미구현되어 항상 0을 반환합니다.'

class_announcements_get_responses = {
    200: openapi.Schema(
        'Announcement List',
        type=openapi.TYPE_OBJECT,
        description='pagination이 적용되어 있습니다. '
                    '시간 역순으로 한 번에 10개의 공지글을 불러옵니다.\n',
        properties={
            'next': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='다음 10개의 공지글을 불러올 api 주소를 담고 있습니다.\n'
                            '만약 현재 불러온 공지글들이 마지막이라면, null 값을 갖습니다.',
            ),
            'previous': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='이전 10개의 공지글을 불러올 api 주소를 담고 있습니다.\n'
                            '처음 10개의 공지글을 불러왔을 때는, 이전 10개의 공지글이 없으므로 null 값을 갖습니다.',
            ),
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Announcement',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            read_only=True,
                        ),
                        'title': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='공지글 제목입니다.',
                        ),
                        'content': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='공지글 내용입니다. 현재는 단순히 리스트를 보는 것이므로, 앞의 10글자만을 반환합니다.',
                        ),
                        'created_by': openapi.Schema(
                            'User',
                            type=openapi.TYPE_OBJECT,
                            description='공지글을 작성한 사용자의 정보입니다.',
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
                                ),
                            },
                        ),
                        'created_at': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='timestamp 형식으로 공지글 생성 시간을 반환합니다.'
                        ),
                        'comment_count': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='해당 공지글에 달린 댓글 수입니다.'
                        ),
                    }
                )
            )
        }
    )
}

class_announcements_post_operation_description = '기능\n' \
                                                 '- 특정 수업에서 공지사항 하나를 생성합니다.\n' \
                                                 '- {id}에는 class id가 들어갑니다.\n' \
                                                 '\npermission\n' \
                                                 '- admin 계정\n' \
                                                 '- 로그인하고, 개인정보가 모두 세팅되었고, 교수인 사용자.\n' \
                                                 '\nrequest body\n' \
                                                 '- title(필수)\n' \
                                                 '- content(필수)\n' \
                                                 '\nresponses\n' \
                                                 '- 201: {id}에 해당하는 수업에 공지사항 하나 생성 성공.'

class_announcements_post_request_body = openapi.Schema(
    'Announcement',
    type=openapi.TYPE_OBJECT,
    description='생성할 공지글의 정보를 입력합니다.',
    required=['title', 'content'],
    properties={
        'title': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='공지글 제목입니다.',
        ),
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='공지글 내용입니다.',
        ),
    },
)

class_announcements_post_responses = {
    201: openapi.Schema(
        'Announcement',
        type=openapi.TYPE_OBJECT,
        description='공지글이 잘 생성되었을 시, 201 status code와 방금 생성한 공지글 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='공지글 제목입니다.',
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='공지글 내용입니다. 앞의 10글자만을 반환합니다.',
            ),
            'created_by': openapi.Schema(
                'User',
                type=openapi.TYPE_OBJECT,
                description='공지글을 작성한 사용자의 정보입니다.',
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
                    ),
                },
            ),
            'created_at': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='timestamp 형식으로 공지글 생성 시간을 반환합니다.'
            ),
            'comment_count': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='해당 공지글에 달린 댓글 수입니다.'
            ),
        }
    )
}
