


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class MyPage(PageNumberPagination):
    page_query_param = 'page' # ?page=2
    page_size_query_param = 'pagesize' # ?pagesize=5
    max_page_size = 10
    page_size = 5 # 默认后台按照每页5个去分页

    # 自定义分页器构建响应数据的格式，以符合接口定义
    def get_paginated_response(self, data):
        return Response({
            'counts': self.page.paginator.count, # 当前分页所有数据量
            'lists': data,
            'page': self.page.number, # 当前页数
            'pages': self.page.paginator.num_pages, # 总页数
            'pagesize': self.page_size, # 后端默认每页数
        })