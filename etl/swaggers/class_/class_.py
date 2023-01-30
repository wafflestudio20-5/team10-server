from drf_yasg.openapi import *

class_get_operation_description = '기능\n' \
                                  '- 특정 수업의 정보를 가져옵니다.\n' \
                                  '- URL의 {id}에는 특정 수업의 id 값이 들어갑니다.\n' \
                                  '\npermission\n' \
                                  '- admin 계정\n' \
                                  '- 로그인 && 개인정보 세팅 완료\n' \
                                  '\nrequest body\n' \
                                  '- 아무것도 없습니다.\n' \
                                  '\nresponses\n' \
                                  '- 200: 특정 수업의 정보 가져오기 성공\n'

class_patch_operation_description = '기능\n' \
                                    '- 특정 수업의 정보를 수정합니다.\n' \
                                    '- URL의 {id}에는 특정 수업의 id 값이 들어갑니다.\n' \
                                    '\npermission\n' \
                                    '- admin 계정\n' \
                                    '- 로그인 && 개인정보 세팅 완료 & 해당 수업을 생성한 사용자\n' \
                                    '\nrequest body\n' \
                                    '- name(선택)\n' \
                                    '\nresponses\n' \
                                    '- 200: 특정 수업의 정보 수정 성공. 수정이 반영된 정보 반환.'

class_patch_request_body = Schema(
    'Class PATCH',
    type=TYPE_OBJECT,
    properties={
        'name': Schema(
            type=TYPE_STRING,
            description='새롭게 설정될 수업 이름입니다.'
        )
    }
)

class_patch_responses = {
    200: Schema(
        'Class',
        type=TYPE_OBJECT,
        description='수정이 완료된 수업 정보를 반환합니다.',
        properties={
            'id': Schema(
                type=TYPE_INTEGER,
                read_only=True,
            ),
            'name': Schema(
                type=TYPE_STRING,
                description='수업 이름입니다.',
            ),
            'created_by': Schema(
                type=TYPE_OBJECT,
                description='수업을 생성한 사람의 정보입니다.',
                properties={
                    'username': Schema(
                        type=TYPE_STRING,
                    )
                }
            ),
        }
    )
}

class_delete_operation_description = '기능\n' \
                                     '- 수업 하나 삭제\n' \
                                     '- URL의 {id}는 삭제할 수업의 id 값이 들어갑니다.\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 로그인 && 개인정보 세팅 완료 && 해당 수업을 생성한 사용자\n' \
                                     '\nrequest body\n' \
                                     '- 아무것도 없습니다.\n' \
                                     '\nresponses\n' \
                                     '- 204: 수업 하나 삭제 성공'
