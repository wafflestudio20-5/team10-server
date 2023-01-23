from drf_yasg import openapi

assignments_class_get_operation_description = '기능\n' \
                                        '- 특정 Assignment의 정보를 불러옵니다.\n' \
                                        '- {id}에는 Assignment id가 들어갑니다. 이는 Class와 관련 없이 생성된 모든 Assignment 기준 id입니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200: assignment detail'

assignments_class_put_operation_description = '기능\n' \
                                        '- 특정 Assignment를 수정합니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 해당 과제를 생성한 사용자\n' \
                                        '\nrequest body\n' \
                                        '<Content-Type : multipart/form-data>\n' \
                                        '- 수업 id\n' \
                                        '- 과제 이름\n' \
                                        '- 마감 기한\n' \
                                        '- 최대 점수\n' \
                                        '- 가중치(0과 1사이의 실수)\n' \
                                        '- 과제 파일(선택)\n'    \
                                        '\nresponse\n' \
                                        '- 201: 수정된 assignment detail'

assignments_class_patch_operation_description = '기능\n' \
                                        '- 특정 Assignment를 부분 수정합니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 해당 과제를 생성한 사용자\n' \
                                        '\nrequest body\n' \
                                        '<Content-Type : multipart/form-data>\n' \
                                        '- 수업 id\n' \
                                        '- 과제 이름\n' \
                                        '- 마감 기한\n' \
                                        '- 최대 점수\n' \
                                        '- 가중치(0과 1사이의 실수)\n' \
                                        '- 과제 파일(선택)\n'    \
                                        '\nresponse\n' \
                                        '- 201:  수정된 assignment detail'

assignments_class_delete_operation_description = '기능\n' \
                                        '- 특정 Assignment를 삭제합니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 해당 과제를 생성한 사용자\n' \
                                        '\nrequest body\n' \
                                        '- 없습니다.\n'    \
                                        '\nresponse\n' \
                                        '-204:  assignment 삭제 성공'
