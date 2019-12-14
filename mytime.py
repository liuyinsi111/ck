

# 关于Python中的时间
from datetime import datetime,timedelta,timezone

# 时间这样一个抽象的东西有哪些属性
# 属性：年月日，时分秒，微妙。时区

# 时间的描述
# 1、上海本地时间2019年12月11日10点51分30秒   -->  时间点(某一个时刻)
tz_shanghai = timezone(offset=timedelta(hours=8)) # 时区对象
cur_time = datetime(year=2019,
                    month=12,
                    day=11,
                    hour=10,
                    minute=51,
                    second=30,
                    microsecond=123456,
                    tzinfo=tz_shanghai)

# print(cur_time)

# 2、一天，一月，一年                       -->  时间段(一段时间)
delta_8_hours = timedelta(hours=8) # 8个小时
delta_5_days = timedelta(days=5) # 5天




# 思考：时间的运算？！
# 理念：数据的类型，决定了可以对数据进行哪些运算

# 时间点
# 时间点A - 时间点B = 时间段C
deltaC = datetime(year=2019, month=12, day=11, hour=11) - datetime(year=2019, month=12, day=11, hour=8)
print("deltaC: ", deltaC, "type: ", type(deltaC))

# 时间段
# 时间段D + 时间段E = 时间段F
deltaF = timedelta(days=1) + timedelta(hours=10)
print("deltaF: ", deltaF, "type: ", type(deltaF))
# 时间段G - 时间段H = 时间段I
deltaI = timedelta(days=1) - timedelta(hours=10)
print("deltaI: ", deltaI, "type: ", type(deltaI))
# 时间段I * 5 = 时间段J
deltaJ = deltaI * 5
print("deltaJ: ", deltaJ, "type: ", type(deltaJ))
# 时间段J / 2 = 时间段K
deltaK = deltaJ / 2
print("deltaK: ", deltaK, "type: ", type(deltaK))


# 时间段K + 时间点 = 时间点
calc_time = deltaK + datetime(year=2019, month=12, day=11, hour=11)
print("calc_time: ", calc_time)
