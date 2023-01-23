from drf_yasg import openapi

module_content_post_operation_description = '기능\n' \
                                        '- 특정 주차학습에 속한 모듈 파일을 생성합니다.\n' \
                                        '- 모듈 파일 id는 각각 속한 주차학습과 관련없이 모든 모듈 파일들의 순서로 배정됩니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인 && 개인정보 세팅 완료 && 교수\n' \
                                        '\nrequest body\n' \
                                        '<Content-Type : multipart/form-data>\n' \
                                        '- 주차학습 id\n' \
                                        '- 모듈 파일\n' \
                                        '\nresponse\n' \
                                        '- 201: 모듈 파일 생성 성공'
