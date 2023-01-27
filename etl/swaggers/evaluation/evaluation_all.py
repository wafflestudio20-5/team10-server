from drf_yasg import openapi

evaluation_check_get_description =  '기능\n' \
                                     '- 현재 로그인한 사용자가 지정된 수업의 평가를 했는지 반환\n' \
                                     '{id}는 class_id\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 로그인하고, 개인정보를 모두 세팅했고, 학생인 사용자\n' \
                                     '\nrequest body\n' \
                                     '- 없습니다.\n' \
                                     '\nresponses\n' \
                                     '- 200: 평가완료\n' \
                                     '- 404: 평가안함'

evaluation_post_description =        '기능\n' \
                                     '- 현재 로그인한 사용자가 지정된 수업을 평가\n' \
                                     '{id}는 class_id\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 로그인하고, 개인정보를 모두 세팅했고, 학생인 사용자\n' \
                                     '\nrequest body\n' \
                                     '- 객관식 문항 1(1~5 정수)\n' \
                                     '- 객관식 문항 2(1~5 정수)\n' \
                                     '- 객관식 문항 3(1~5 정수)\n' \
                                     '- 객관식 문항 4(1~5 정수)\n' \
                                     '- 객관식 문항 5(1~5 정수)\n' \
                                     '- 객관식 문항 6(1~5 정수)\n' \
                                     '- 객관식 문항 7(1~5 정수)\n' \
                                     '- 주관식 문항 1\n' \
                                     '- 주관식 문항 2\n' \
                                     '\nresponses\n' \
                                     '- 201: 강의평가 성공'
