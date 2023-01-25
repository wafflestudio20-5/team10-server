from rest_framework.pagination import CursorPagination, PageNumberPagination


class StudentListPagination(PageNumberPagination):
    page_size = 5


class PostListPagination(PageNumberPagination):
    page_size = 10


class ClassListPagination(PageNumberPagination):
    page_size = 10

