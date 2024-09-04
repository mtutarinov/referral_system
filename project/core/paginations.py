from rest_framework.pagination import CursorPagination

class CorePagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'
    max_page_size = 100