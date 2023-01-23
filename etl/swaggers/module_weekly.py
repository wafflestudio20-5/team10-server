from drf_yasg import openapi

module_weekly_post_operation_description = '기능\n' \
                                        '- 특정 Class Module에 새 주차학습을 생성합니다.\n' \
                                        '- 주차학습의 id는 각각 속한 Class Module과 관련없이 모든 주차학습들의 순서로 배정됩니다.\n' \
                                        '\npermission\n' \
                                        '- admin\n' \
                                        '- professor\n' \
                                        '\nrequest body\n' \
                                        '- module id\n' \
                                        '- 주차학습 이름\n' \
                                        '\nresponse\n' \
                                        '- 201:  주차학습 생성 성공'