from drf_yasg import openapi

assignments_list_lecture_get_operation_description = '기능\n' \
                                        '- 특정 Class의 Assignment들의 List를 반환합니다.\n' \
                                        '- {id}에는 Class id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- 로그인된 유저\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200:  assignment list'

assignments_list_student_get_operation_description = '기능\n' \
                                        '- 접속한 User에게 주어진 Assignment들의 List를 반환합니다.\n' \
                                        '\npermission\n' \
                                        '- 로그인된 유저\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200:  assignment list'