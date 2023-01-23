from drf_yasg import openapi

assignments_upload_put_operation_description = '기능\n' \
                                        '- 로그인 한 User가 특정 Assignment에 과제를 업로드합니다.\n' \
                                        '- {id}에는 Assignment id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료\n' \
                                        '\nrequest body\n' \
                                        '<Content-Type : multipart/form-data>\n' \
                                        '- 과제 제출 파일\n' \
                                        '\nresponse\n' \
                                        '- 201: 제출 성공'

assignments_download_get_operation_description = '기능\n' \
                                        '- 로그인 한 User가 특정 Assignment에 제출했던 과제를 다운로드합니다.\n' \
                                        '- {id}에는 Assignment id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200: 과제 제출 파일'


assignments_user_download_get_operation_description = '기능\n' \
                                        '- user_pk번째 학생의 id번째 과제의 제출물을 다운로드합니다..\n' \
                                        '- {id}에는 Assignment id가 들어갑니다.\n'\
                                        '- {user_pk}에는 User id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 해당 과제를 생성한 사용자\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200: 과제 제출 파일'
