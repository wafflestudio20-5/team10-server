from drf_yasg import openapi

class_enroll_operation_description = '기능\n' \
                                     '- 현재 로그인한 사용자가 수업 하나를 수강신청\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 로그인하고, 개인정보를 모두 세팅했고, 학생인 사용자\n' \
                                     '\nrequest body\n' \
                                     '- class_id(필수)\n' \
                                     '- user_id를 입력하지 않아도, 현재 token을 바탕으로 현재 요청을 넣는 사용자를 구분합니다.\n' \
                                     '\nresponses\n' \
                                     '- 201: 수강신청 성공'

class_enroll_request_body = openapi.Schema(
    'Enroll Class',
    type=openapi.TYPE_OBJECT,
    required=['class_id'],
    properties={
        'class_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='수강신청할 수업의 id'
        ),
    },
)

class_enroll_responses = {
    201: openapi.Schema(
        'Success',
        type=openapi.TYPE_OBJECT,
        description='방금 전 수행한 수강신청을 반영한 현재 사용자의 수강하는 수업 리스트를 반환합니다.',
        properties={
            'classes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            read_only=True,
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='수업 이름',
                        ),
                    }
                )
            )
        },
    )
}

class_drop_operation_description = '기능\n' \
                                     '- 현재 로그인한 사용자가 수업 하나를 수강취소\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 로그인하고, 개인정보를 모두 세팅했고, 학생인 사용자\n' \
                                     '\nrequest body\n' \
                                     '- class_id(필수)\n' \
                                     '- user_id를 입력하지 않아도, 현재 token을 바탕으로 현재 요청을 넣는 사용자를 구분합니다.\n' \
                                     '\nresponses\n' \
                                     '- 201: 수강취소 성공'

class_drop_request_body = openapi.Schema(
    'Drop Class',
    type=openapi.TYPE_OBJECT,
    required=['class_id'],
    properties={
        'class_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='수강취소할 수업의 id'
        ),
    },
)

class_drop_responses = {
    201: openapi.Schema(
        'Success',
        type=openapi.TYPE_OBJECT,
        description='방금 전 수행한 수강취소를 반영한 현재 사용자의 수강하는 수업 리스트를 반환합니다.',
        properties={
            'classes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            read_only=True,
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='수업 이름',
                        ),
                    }
                )
            )
        },
    )
}

# TODO: 페이지네이션 적용 후 비고 삭제
class_get_operation_description = '기능\n' \
                                  '- 모든 존재하는 수업 목록을 불러옵니다.\n' \
                                  '\n권한\n' \
                                  '- admin 계정\n' \
                                  '- 로그인한 사용자\n' \
                                  '\nrequest body\n' \
                                  '- 아무것도 없습니다.\n' \
                                  '\nresponses\n' \
                                  '- 200: 모든 수업 목록 받아오기 성공\n' \
                                  '\n비고\n' \
                                  '- 아직 pagination을 적용하지 않았습니다.'

class_post_operation_description = '기능\n' \
                                   '- 수업 하나를 생성합니다.\n' \
                                   '\npermission\n' \
                                   '- admin 계정\n' \
                                   '- 로그인하고, 교수인 사용자\n' \
                                   '\nrequest body\n' \
                                   '- 수업 이름(필수)\n' \
                                   '\nresponses\n' \
                                   '- 201: 수업 하나 생성 성공'

class_post_request_body = openapi.Schema(
    'Class',
    type=openapi.TYPE_OBJECT,
    required=['name'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING)
    }
)

class_post_responses = {
    201: openapi.Schema(
        'Class',
        type=openapi.TYPE_OBJECT,
        description='방금 생성된 수업 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='수업 이름',
            ),
            'created_by': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='수업을 생성한 사람의 정보. 생성한 사람의 이름만 반환합니다.',
                properties={
                    'username': openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                }
            )
        }
    )
}

class_professor_get_operation_description = '기능\n' \
                                            '- 현재 사용자가 생성한 수업 리스트 조회\n' \
                                            '\npermission\n' \
                                            '- admin 계정\n' \
                                            '- 로그인하고, 개인정보를 모두 세팅했고, 교수인 사용자\n' \
                                            '\nrequest body\n' \
                                            '- 아무것도 없습니다.\n' \
                                            '\nresponses\n' \
                                            '- 200: 수업 리스트 조회 성공'

class_professor_post_operation_description = '기능\n' \
                                             '- 수업 생성\n' \
                                             '\npermission\n' \
                                             '- admin 계정\n' \
                                             '- 로그인하고, 개인정보를 모두 세팅했고, 교수인 사용자\n' \
                                             '\nrequest body\n' \
                                             '- name(필수)\n' \
                                             '\nresponses\n' \
                                             '- 201: 수업 생성 성공\n' \
                                             '\n비고\n' \
                                             '- 사실 /etl/class/에 POST 요청을 넣는 것과 동작이 동일합니다.'

class_professor_post_responses = class_post_responses

class_delete_operation_description = '기능\n' \
                                     '- 수업 하나 삭제\n' \
                                     '- URL의 {id}는 삭제할 수업의 id 값이 들어갑니다.\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 해당 수업을 생성한 사용자\n' \
                                     '\nrequest body\n' \
                                     '- 아무것도 없습니다.\n' \
                                     '\nresponses\n' \
                                     '- 204: 수업 하나 삭제 성공'

class_user_list_operation_description = '기능\n' \
                                        '- 특정 수업을 듣고 있는 수강생 리스트를 반환\n' \
                                        '- URL의 {id}에는 수업의 id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인하고, 개인정보 세팅이 모두 완료된 사용자\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 없습니다.\n' \
                                        '\nresponses\n' \
                                        '- 200: 특정 수업의 수강생 리스트 반환 성공\n' \
                                        '\n비고\n' \
                                        '- 용이한 pagination 테스트를 위해, 한 번에 2명씩 수강생 정보를 가져옵니다.\n' \
                                        '- pagination 정렬 순서는 username 사전순입니다.'

class_user_list_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'next': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='다음 2명의 수강생을 불러올 api 주소를 담고 있습니다.\n'
                            '만약 현재 불러온 수강생들이 마지막이라면, null 값을 갖습니다.',
            ),
            'previous': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='이전 2명의 수강생을 불러올 api 주소를 담고 있습니다.\n'
                            '처음 수강생을 불러왔을 때는, 이전 2명의 수강생이 없으므로 null 값을 갖습니다.',
            ),
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'User',
                    type=openapi.TYPE_OBJECT,
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
                    }
                )
            )
        }
    )
}

user_list_operation_description = '모든 유저의 정보를 불러옵니다.\n' \
                                  '본래 개발 중 디버깅 용으로 사용하기 위해 admin 계정에만 GET 요청을 허용했습니다.\n' \
                                  '모든 유저의 정보를 list로 담아옵니다.'

assignment_grading_put_operation_description = 'Assignment 채점 : 교수자가 id번째 Assignment의 성적을 해당 학생의 user_id, 점수를 입력해 채점'

assignment_grading_patch_operation_description = "Assignment 채점 : 교수자가 id번째 Assignment의 성적을 해당 학생의 user_id, 점수를 입력해 채점"

assignments_get_operation_description = '기능\n' \
                                        '- 모든 Assignment List를 반환합니다.\n' \
                                        '- 현재 유저가 듣는 수업과 상관없이, 모든 Assignment list를 반환합니다.\n' \
                                        '\npermission\n' \
                                        '- 로그인된 유저\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- assignment list'

announcement_get_operation_description = '기능\n' \
                                         '- 공지사항 하나의 정보를 자세히 가져옵니다.\n' \
                                         '- URL의 {id}에는 공지사항의 id가 들어갑니다.\n' \
                                         '\npermission\n' \
                                         '- admin 계정\n' \
                                         '- 로그인하고, 개인정보가 모두 세팅되어있는 사용자\n' \
                                         '\nrequest body\n' \
                                         '- 아무것도 담지 않습니다.\n' \
                                         '\nresponses\n' \
                                         '- 200: 공지사항 하나의 정보 가져오기 성공\n' \
                                         '\n비고\n' \
                                         '- created_at은 생성 시간으로, timestamp를 반환합니다.\n' \
                                         '- comments는 해당 공지사항에 달린 comment 리스트입니다.'

announcement_patch_operation_description = '기능\n' \
                                         '- 공지사항 하나의 정보를 수정합니다.\n' \
                                         '- URL의 {id}에는 공지사항의 id가 들어갑니다.\n' \
                                         '\npermission\n' \
                                         '- admin 계정\n' \
                                         '- 로그인하고, 개인정보가 모두 세팅되어 있고, 해당 공지사항을 작성한 사용자\n' \
                                         '\nrequest body\n' \
                                         '- title(선택)\n' \
                                         '- content(선택)\n' \
                                         '\nresponses\n' \
                                         '- 200: PATCH 성공, 공지사항 하나의 정보 가져옴'

post_patch_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
        )
    },
    description='title이나 content를 수정합니다.'
)

post_detail_responses = {
    200: openapi.Schema(
        'Post Detail',
        type=openapi.TYPE_OBJECT,
        description='게시글의 세부정보입니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='게시글 제목입니다.',
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='게시글 내용입니다. 특정 수업에 속한 게시글 리스트를 불러올 때와 다르게 문자열을 자르지 않고 모두 반환합니다.',
            ),
            'created_by': openapi.Schema(
                'User',
                type=openapi.TYPE_OBJECT,
                description='해당 게시글을 생성한 사람의 정보입니다.',
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
            'comments': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='해당 게시글에 달린 댓글 리스트입니다.',
                items=openapi.Schema(
                    'Comment',
                    type=openapi.TYPE_OBJECT,
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
                            description='timestamp 형식으로 댓글 생성 시간을 반환합니다.'
                        ),
                    }
                )
            )
        }
    )
}

announcement_delete_operation_description = '기능\n' \
                                    '- 공지사항 하나 삭제\n' \
                                    '- {id}에 해당하는 게시글 하나를 삭제합니다.\n' \
                                    '\npermission\n' \
                                    '- admin 계정\n' \
                                    '- 로그인하고, 개인정보가 모두 세팅되어 있고, 해당 공지사항을 작성한 사용자\n' \
                                    '\nrequest body\n' \
                                    '- 아무것도 없습니다.\n' \
                                    '\nresponses\n' \
                                    '- 204: {id}에 해당하는 공지사항 하나 삭제 성공'

# TODO: 댓글 갯수 기능 추가 후 비고 삭제
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
                                                '- 해당 공지사항에 달린 댓굴의 갯수를 가져올 수 있도록 기능을 추가할 예정입니다.'

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

post_list_responses = {
    200: openapi.Schema(
        'Post List',
        type=openapi.TYPE_OBJECT,
        description='pagination이 적용되어 있습니다. '
                    '시간 역순으로 한 번에 10개의 게시글을 불러옵니다.\n',
        properties={
            'next': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='다음 10개의 게시글을 불러올 api 주소를 담고 있습니다.\n'
                            '만약 현재 불러온 게시글들이 마지막이라면, null 값을 갖습니다.',
            ),
            'previous': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='이전 10개의 게시글을 불러올 api 주소를 담고 있습니다.\n'
                            '처음 10개의 게시글을 불러왔을 때는, 이전 10개의 개시글이 없으므로 null 값을 갖습니다.',
            ),
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Post',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            read_only=True,
                        ),
                        'title': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='게시글 제목입니다.',
                        ),
                        'content': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='게시글 내용입니다. 현재는 단순히 리스트를 보는 것이므로, 앞의 10글자만을 반환합니다.',
                        ),
                        'created_by': openapi.Schema(
                            'User',
                            type=openapi.TYPE_OBJECT,
                            description='게시글을 작성한 사용자의 정보입니다.',
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
                            description='timestamp 형식으로 게시글 생성 시간을 반환합니다.'
                        ),
                    }
                )
            )
        }
    )
}

post_post_responses = {
    201: openapi.Schema(
        'Post',
        type=openapi.TYPE_OBJECT,
        description='게시글이 잘 생성되었을 시, 201 status code와 방금 생성한 게시글 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='게시글 제목입니다.',
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='게시글 내용입니다. 앞의 10글자만을 반환합니다.',
            ),
            'created_by': openapi.Schema(
                'User',
                type=openapi.TYPE_OBJECT,
                description='게시글을 작성한 사용자의 정보입니다.',
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
                description='timestamp 형식으로 게시글 생성 시간을 반환합니다.'
            ),
        }
    )
}

post_post_request_body = openapi.Schema(
    'Post',
    type=openapi.TYPE_OBJECT,
    description='생성할 게시글의 정보를 입력합니다.',
    required=['title', 'content'],
    properties={
        'title': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='게시글 제목입니다.',
        ),
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='게시글 내용입니다.',
        ),
    },
)

# TODO: 댓글 갯수 기능 추가 후 비고 삭제
class_questions_get_operation_description = '기능\n' \
                                           '- 특정 수업에 해당하는 질문글 목록을 가져옵니다.\n' \
                                            '- {id}에는 class id가 들어갑니다.\n' \
                                            '- 페이지네이션이 적용되어 있습니다. 한 번에 질문글 10개씩, 최근 순으로 가져옵니다.\n' \
                                            '\npermission\n' \
                                            '- admin 계정\n' \
                                            '- 로그인하고, 개인정보가 모두 세팅된 사용자\n' \
                                            '\nrequest body\n' \
                                            '- 아무것도 없습니다.\n' \
                                            '\nresponses\n' \
                                            '- 200: {id}에 해당하는 수업의 딜문글 목록 가져오기 성공\n' \
                                            '\n비고\n' \
                                            '- 해당 질문글에 달린 댓글의 갯수를 가져올 수 있도록 기능을 추가할 예정입니다.'

class_questions_post_operation_description = '기능\n' \
                                                 '- 특정 수업에서 질문글 하나를 생성합니다.\n' \
                                                 '- {id}에는 class id가 들어갑니다.\n' \
                                                 '\npermission\n' \
                                                 '- admin 계정\n' \
                                                 '- 로그인하고, 개인정보가 모두 세팅된 사용자\n' \
                                                 '\nrequest body\n' \
                                                 '- title(필수)\n' \
                                                 '- content(필수)\n' \
                                                 '\nresponses\n' \
                                                 '- 201: {id}에 해당하는 수업에 질문글 하나 생성 성공.\n'

question_get_operation_description = '기능\n' \
                                         '- 질문글 하나의 정보를 자세히 가져옵니다.\n' \
                                         '- URL의 {id}에는 질문글의 id가 들어갑니다.\n' \
                                         '\npermission\n' \
                                         '- admin 계정\n' \
                                         '- 로그인하고, 개인정보가 모두 세팅되어있는 사용자\n' \
                                         '\nrequest body\n' \
                                         '- 아무것도 담지 않습니다.\n' \
                                         '\nresponses\n' \
                                         '- 200: 질문글 하나의 정보 가져오기 성공\n' \
                                         '\n비고\n' \
                                         '- created_at은 생성 시간으로, timestamp를 반환합니다.\n' \
                                         '- comments는 해당 질문에 달린 comment 리스트입니다.'

question_patch_operation_description = '기능\n' \
                                         '- 질문글 하나의 정보를 수정합니다.\n' \
                                         '- URL의 {id}에는 질문글의 id가 들어갑니다.\n' \
                                         '\npermission\n' \
                                         '- admin 계정\n' \
                                         '- 로그인 && 개인정보 세팅 완료 && (교수자 || 질문글 작성자)\n' \
                                         '\nrequest body\n' \
                                         '- title(선택)\n' \
                                         '- content(선택)\n' \
                                         '\nresponses\n' \
                                         '- 200: PATCH 성공, 질문글 하나의 정보 가져옴'

question_delete_operation_description = '기능\n' \
                                    '- 질문글 하나 삭제\n' \
                                    '- {id}에 해당하는 질문글 하나를 삭제합니다.\n' \
                                    '\npermission\n' \
                                    '- admin 계정\n' \
                                    '- 로그인 && 개인정보 세팅 완료 && (교수자 || 질문글 작성자)\n' \
                                    '\nrequest body\n' \
                                    '- 아무것도 없습니다.\n' \
                                    '\nresponses\n' \
                                    '- 204: {id}에 해당하는 질문글 하나 삭제 성공'

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

comment_get_operation_description = '기능\n' \
                                    '- 특정 댓글의 정보를 가져옵니다.\n' \
                                    '- URL의 {id}에는 댓글의 id가 들어갑니다.\n' \
                                    '\npermission\n' \
                                    '- admin 계정\n' \
                                    '- 로그인하고, 개인정보 세팅을 완료한 사용자\n' \
                                    '\nrequest body\n' \
                                    '- 아무것도 없습니다.\n' \
                                    '\nresponses\n' \
                                    '- 200: 특정 댓글의 정보 가져오기 성공\n' \
                                    '\n비고\n' \
                                    '- Django에서 API 생성을 도와주는 라이브러리가 있어 생성하긴 하였으나, 당장은 GET 요청이 필요하지는 않을 것 같습니다.\n' \
                                    '본래 이런 API에서는 댓글 하나의 세부정보를 볼 수 있도록 지원해야 하나, etl/annuoncement/{id}/ 또는 ' \
                                    'etl/question/{id}/에서 comments에서 얻을 수 있는 정보보다 더 많은 것이 현재로서는 전혀 없습니다.\n' \
                                    '이 GET 요청을 받는 api는 당장은 아무 역할을 하지 않을 것으로 생각됩니다.'

comment_get_responses = {
    200: openapi.Schema(
        'Comment',
        type=openapi.TYPE_OBJECT,
        description='댓글 하나의 정보를 반환합니다.',
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

# TODO: 다음 서버 배포 시 비고 삭제
comment_patch_operation_description = '기능\n' \
                                      '- 특정 댓글의 내용을 수정합니다.\n' \
                                      '- URL의 {id}는 댓글의 id를 의미합니다.\n' \
                                      '\npermission\n' \
                                      '- admin 계정\n' \
                                      '- 로그인 && 개인정보 세팅 완료 && (해당 댓글 작성자 || 교수자)\n' \
                                      '\nrequest body\n' \
                                      '- content(선택)\n' \
                                      '\nresponses\n' \
                                      '- 200: 특정 댓글 내용 수정 성공\n' \
                                      '\n비고\n' \
                                      '- permission을 잘못 설정했습니다. 현재 배포에서는 교수자가 댓글 내용을 수정할 수 없습니다. 다음 배포 때 고치겠습니다.'

comment_patch_request_body = openapi.Schema(
    'Comment',
    type=openapi.TYPE_OBJECT,
    properties={
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='댓글 내용입니다.',
        ),
    }
)

comment_patch_responses = {
    200: openapi.Schema(
        'Comment',
        type=openapi.TYPE_OBJECT,
        description='방금 수정된 댓글 정보를 반환합니다.',
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

# TODO: 다음 서버 배포 시 비고 삭제
comment_delete_operation_description = '기능\n' \
                                       '- 특정 댓글을 삭제합니다.\n' \
                                       '- URL의 {id}에는 삭제하고자 하는 댓글의 id가 들어갑니다.\n' \
                                       '\npermission\n' \
                                       '- admin 계정\n' \
                                       '- 로그인 && 개인정보 세팅 완료 && (해당 댓글 작성자 || 교수자)\n' \
                                       '\nrequest body\n' \
                                       '- 아무것도 없습니다.\n' \
                                       '\nresponses\n' \
                                       '- 204: 특정 댓글 삭제 성공\n' \
                                       '\n비고\n' \
                                       '- permission을 잘못 설정했습니다. 현재 배포에서는 교수자가 댓글을 삭제할 수 없습니다. 다음 배포 때 고치겠습니다.'

