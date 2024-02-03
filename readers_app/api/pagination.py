from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination 

# class BookListPagination(PageNumberPagination):
#     page_size =5
#     page_query_param = 'pg'


class BookListLOPagination(LimitOffsetPagination):
    
    default_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'start'
    
# class BookListCurPagination(CursorPagination):
    
    # page_size = 3