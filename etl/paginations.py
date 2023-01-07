from rest_framework.pagination import CursorPagination


class StudentListPagination(CursorPagination):
    ordering = 'username'
    page_size = 2
