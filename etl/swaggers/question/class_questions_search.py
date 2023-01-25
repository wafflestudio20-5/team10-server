from drf_yasg.openapi import *

class_questions_search_operation_description = '기능\n' \
                                               '- 특정 수업의 질문글 검색 기능을 지원합니다.\n' \
                                               '- URL의 {id}에는 특정 수업의 id가 들어갑니다.\n' \
                                               '- 특정 수업의 질문글 "제목"을 검색합니다.\n' \
                                               '- 페이지네이션이 적용되어, 생성시간 역순(최근순)으로 질문글을 ' \
                                               '10개씩 반환합니다.\n' \
                                               '\npermission\n' \
                                               '- admin 계정\n' \
                                               '- 로그인 && 개인정보 세팅 완료\n' \
                                               '\nparameters\n' \
                                               '- name(필수)\n' \
                                               '\nresponses\n' \
                                               '- 200: 질문글 검색 성공\n' \
                                               '\n사용 예시\n' \
                                               '- id=1인 수업에서 "질문" 키워드가 들어간 질문글을 검색하고 싶을 때, ' \
                                               '"baseURL/etl/class/1/questions/search/?name=질문" 사용\n' \
                                               '\n비고\n' \
                                               '- 현재는 질문글의 제목만을 검색합니다. ' \
                                               '내용 검색도 필요하다면, 말씀 바랍니다.'

class_questions_search_responses = {
    200: Schema(
        'Question Search Result',
        type=TYPE_OBJECT,
        properties={
            'next': Schema(
                type=TYPE_STRING,
                description='다음 10개의 잘뮨굴을 불러올 API 주소를 담고 있습니다.\n'
                            '만약 현재 불러온 질문글들이 마지막이라면, null 값을 갖습니다.',
            ),
            'previous': Schema(
                type=TYPE_STRING,
                description='이전 10개의 질문글을 불러올 API 주소를 담고 있습니다.\n'
                            '처음 질문글을 불러왔을 때는, 이전 10개의 질문글이 없으므로 null 값을 갖습니다.',
            ),
            'results': Schema(
                type=TYPE_ARRAY,
                description='질문 검색 결과로 반환되는 리스트입니다.',
                items=Schema(
                    'Question',
                    type=TYPE_OBJECT,
                    properties={
                        'id': Schema(
                            type=TYPE_INTEGER,
                            read_only=True,
                        ),
                        'title': Schema(
                            type=TYPE_STRING,
                            description='질문글 제목입니다.',
                        ),
                        'created_by': Schema(
                            type=TYPE_OBJECT,
                            description='질문글 작성자 정보입니다.\n',
                            properties={
                                'id': Schema(
                                    type=TYPE_INTEGER,
                                    read_only=True,
                                ),
                                'username': Schema(
                                    type=TYPE_STRING,
                                ),
                                'student_id': Schema(
                                    type=TYPE_STRING,
                                ),
                                'is_professor': Schema(
                                    type=TYPE_BOOLEAN,
                                ),
                            },
                        ),
                        'created_at': Schema(
                            type=TYPE_STRING,
                            description='질문글 생성 시간입니다. 13자리 timestamp 형식입니다.'
                        ),
                        'comment_count': Schema(
                            type=TYPE_INTEGER,
                            description='해당 질문글에 달린 댓글 수입니다.'
                        ),
                        'hits': Schema(
                            type=TYPE_INTEGER,
                            description='해당 질문글의 조회수입니다.\n"baseURL/etl/question/{id}/"에 GET 요청을 '
                                        '넣을 때마다, 조회수는 1씩 증가합니다.'
                        ),
                    }
                )
            ),
            'total_question_count': Schema(
                type=TYPE_STRING,
                description='검색 조건을 만족하는 질문글의 갯수입니다.',
            ),
        }
    ),
}

class_questions_search_parameter_name = Parameter(
    'name',
    IN_QUERY,
    description='해당 name을 포함한 제목을 가지고 있는 질문글을 불러옵니다.',
    required=True,
    type=TYPE_STRING,
)

class_questions_search_manual_parameters = [class_questions_search_parameter_name]
