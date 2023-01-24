from drf_yasg import openapi

assignments_grade_get_operation_description = '기능\n' \
                                        '- 로그인 한 User의 특정 Assignment에 대한 점수와 제출 상태를 반환합니다.\n' \
                                        '- {id}에는 Assignment id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '-200: AssignmentToStudent'

assignments_class_total_get_operation_description = '기능\n' \
                                        '- 로그인 한 User의 특정 Class에 속한 모든 Assignment들의 점수와 제출 상태를 반환합니다.\n' \
                                        '- {id}에는 Class id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200: AssignmentToStudent list'

assignments_grading_put_operation_description = '기능\n' \
                                        '- 교수자가 id번째 Assignment에 특정 학생의 점수를 입력합니다.\n' \
                                        '- {id}에는 Assignment id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 해당 과제를 생성한 사용자\n' \
                                        '\nrequest body\n' \
                                        '- 학생의 id\n' \
                                        '- 점수\n' \
                                        '\nresponse\n' \
                                        '- 200: 채점 완료'

assignments_grading_patch_operation_description = '기능\n' \
                                        '- 교수자가 id번째 Assignment에 특정 학생의 점수를 입력합니다.\n' \
                                        '- {id}에는 Assignment id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 해당 과제를 생성한 사용자\n' \
                                        '\nrequest body\n' \
                                        '- 학생의 id\n' \
                                        '- 점수\n' \
                                        '\nresponse\n' \
                                        '- 200: 채점 완료'
