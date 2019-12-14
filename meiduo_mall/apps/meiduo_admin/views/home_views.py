

# 定义主页相关视图


# 用户总数统计
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from orders.models import OrderInfo
from goods.models import GoodsVisitCount

from datetime import datetime,timedelta,timezone
# timezone: django封装的用来处理时间的模块
from django.utils import timezone as dj_timezone
from django.conf import settings
import pytz

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAdminUser

# 原则：一类资源的处理，尽可能定义在一个视图中
class HomeViewSet(ViewSet):
    # permission_classes = [IsAdminUser]


    # 用户总数统计
    @action(methods=['get'], detail=False)
    def total_count(self, request):
        # 1、统计用户模型类对象总数
        count = User.objects.count()
        date = datetime.today() # 年月日

        # 2、构建响应数据返回
        return Response({
            "count": count,
            "date": date
        })

    # 日新增用户统计
    @action(methods=['get'], detail=False)
    def day_increment(self, request):

        # 1、获得"当日"的零时作为过滤的条件
        cur_utctime = datetime.utcnow()  # datetime对象,表示当前时刻(是以utc时区作为表示形式的)
        # utcnow()：函数得到0时区时刻， 但是会丢弃时区属性
        # print("utc时间:", cur_utctime)
        # 1.1 要把utc(+00:00) 转化成东八区(+8:00)
        cur_localtime = cur_utctime + timedelta(hours=8)
        # print("东八区时间: ", cur_localtime)
        # cur_localtime: 东八区当前时刻;需要转化成0时，并添加时区属性
        # 2019-12-11 00:00:00.000000+08:00
        cur_0_localtime = cur_localtime.replace(hour=0, minute=0, second=0, microsecond=0,
                                                tzinfo=timezone(timedelta(hours=8)))

        # print(cur_0_localtime)

        # 2、过滤统计出今天新建的用户总数
        count = User.objects.filter(date_joined__gte=cur_0_localtime).count()
        # 3、构建响应数据返回
        return Response({
            "count":count,
            "date": cur_0_localtime.date() # 只取年月日
        })

    # 日活跃用户统计
    @action(methods=['get'], detail=False)
    def day_active(self, request):

        # 1、获得"当日"(当前django服务器所在时区)的零时
        # 获得'Asia/Shanghai'的当日零时
        # 当前时刻: 2019-12-11 03:56:31.219005+00:00
        # django.utils.timezone.now()得到的是当前时刻，是utc零时区所描述的当前时刻
        cur_time = dj_timezone.now()
        # 1.1 把cur_time这个utc时区时间转化成'Asia/Shanghai'时区的时刻
        cur_shanghai_time = cur_time.astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        # 1.2 获得本地的零时
        cur_0_shanghai = cur_shanghai_time.replace(hour=0,
                                                   minute=0,
                                                   second=0,
                                                   microsecond=0)

        # print("通过django接口获得当前时间：", cur_0_shanghai)

        # 2、过滤当日活跃用户数
        count = User.objects.filter(last_login__gte=cur_0_shanghai).count()

        # 3、构建响应数据返回
        return Response({
            "count": count,
            "date": cur_0_shanghai.date()
        })

    # 当日下单用户统计
    # 日下单用户统计：大于等于今天零时的所有订单(从表)，查询所有订单关联的用户(主表)
    @action(methods=['get'], detail=False)
    def day_orders(self, request):

        # 联合查询User、OrderInfo
        # 分析：
        # 1）目标数据;  答：User表(主表数据)
        # 2）已知条件;  答：当日零时作为已知条件，过滤出今天下的订单OrderInfo(从表数据)


        # 当日零时
        cur_time = dj_timezone.now()
        # 1.1 把cur_time这个utc时区时间转化成'Asia/Shanghai'时区的时刻
        cur_shanghai_time = cur_time.astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        # 1.2 获得本地的零时
        cur_0_shanghai = cur_shanghai_time.replace(hour=0,
                                                   minute=0,
                                                   second=0,
                                                   microsecond=0)


        # 方案一
        # 从从表入手查询
        # 1 已知条件是从表，先查询出所有从表数据对象(查询出所有当日下的订单对象查询集)
        # order_queryset = OrderInfo.objects.filter(create_time__gte=cur_0_shanghai)
        # 2、从从表数据对象中，提取下单的用户(主表数据提取)
        # user_set = set() # 集合过滤重复下单的用户
        # for order in order_queryset:
            # order: 每一个订单对象
            # user_set.add(order.user)
        # return Response({
        #     "count": len(user_set),
        #     "date": cur_0_shanghai.date()
        # })

        # 方案二
        # 从主表入手查询
        # 在django的模型类中，允许我们使用从表已知条件查询主表目标数据
        # user_queryset:指的是所有过滤出来的从表对象中提取的主表对象，未去重
        user_queryset = User.objects.filter(orders__create_time__gte=cur_0_shanghai) # 过滤出当日下单的用户们
        # 去重
        count = len(set(user_queryset))

        return Response({
            "count": count,
            "date": cur_0_shanghai.date()
        })

    # 最近30日增用户统计
    # 统计最近包括当日新增用户量
    @action(methods=['get'], detail=False)
    def month_increment(self, request):

        # 本地时间零时
        # 当日零时
        cur_time = dj_timezone.now()
        # 1.1 把cur_time这个utc时区时间转化成'Asia/Shanghai'时区的时刻
        cur_shanghai_time = cur_time.astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        # 1.2 获得本地的零时
        cur_0_shanghai = cur_shanghai_time.replace(hour=0,
                                                   minute=0,
                                                   second=0,
                                                   microsecond=0)

        # 1、把过去30天，每一天的零时计算出来
        # end_0_time <= cur_time <= start_0_time 总共是三十天的零时
        end_0_time = cur_0_shanghai # 最后一天的零时
        start_0_time = end_0_time - timedelta(days=29)


        return_list = []
        # 1.1 分别计算出30天中每一天零时
        for index in range(30): # 0<=index<=29
            # 遍历三十次，分别得到每一天的零时
            # 第一天： start_0_time + 零天 --> start_0_time + timedelta(days=0)   index=0
            # 第二天： start_0_time + 一天 --> start_0_time + timedelta(days=1)   index=1
            # 第三天： start_0_time + 二天 --> start_0_time + timedelta(days=2)   index=2
            # ......
            # 第30天： start_0_time + 29天 --> start_0_time + timedelta(days=29)   index=29

            # calc_0_time: 就是30天中某一天的零时
            calc_0_time = start_0_time + timedelta(days=index)

            # next_0_time: 过去某一天的次日零时
            next_0_time = calc_0_time + timedelta(days=1)

            # 2、根据每日的零时，过滤出当天新增的用户
            count = User.objects.filter(
                date_joined__gte=calc_0_time,
                date_joined__lt=next_0_time
            ).count()

            return_list.append({
                "count": count,
                "date": calc_0_time.date()
            })


        # 3、构建数据返回
        return Response(return_list)




from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.home_serializers import GoodsVisitCountModelSerializer
# 序列化返回GoodsVisitCount模型类对象多条数据
class GoodsVisitCountView(ListAPIView):
    # permission_classes = [IsAdminUser]

    queryset = GoodsVisitCount.objects.all()
    serializer_class = GoodsVisitCountModelSerializer

    def get_queryset(self):
        # 针对每一次请求。都会调用该方法
        # 我们需要在该方法中，获得零时，并过滤
        # 当日零时
        cur_time = dj_timezone.now()
        # 1.1 把cur_time这个utc时区时间转化成'Asia/Shanghai'时区的时刻
        cur_shanghai_time = cur_time.astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        # 1.2 获得本地的零时
        cur_0_shanghai = cur_shanghai_time.replace(hour=0,
                                                   minute=0,
                                                   second=0,
                                                   microsecond=0)

        # 数据集要求是今天的访问数据
        queryset = GoodsVisitCount.objects.filter(create_time__gte=cur_0_shanghai)

        return queryset













