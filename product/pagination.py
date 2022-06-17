from rest_framework import pagination

class ProductPagination(pagination.PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'count'
    max_page_size = 12
