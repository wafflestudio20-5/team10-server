from drf_yasg import openapi

module_class_get_operation_description = '기능\n' \
                                        '- 특정 Class의 Module 정보를 List로 반환합니다.\n' \
                                        '- 주차학습 -> 각 파일의 계층 구조로 되어있습니다.\n' \
                                        '- {id}에는 Class id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- 로그인된 유저\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 담지 않습니다.\n' \
                                        '\nresponse\n' \
                                        '- 200:  module list'
