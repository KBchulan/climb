from climb import climb_data_xinlang
from data_to_mysql import save_to_mysql
from show_base import show_data_with_qt
from show_base import show_data_with_imgui
from show_base import show_data_with_pandas
from k_line import plot_kline

code = "sh600000"
timeout = 60
datalen = 2000

database = "pywork"

# 获取到信息
data_for_k_line_pd = climb_data_xinlang(code, timeout, datalen)
data_for_gl = climb_data_xinlang(code, timeout, 500)

# 保存到数据库,使用时去掉注释即可
save_to_mysql(data_for_k_line_pd, database)
save_to_mysql(data_for_gl, database)

# 绘制表格
show_data_with_qt()
show_data_with_imgui()
show_data_with_pandas()

# 绘制K线图
plot_kline('pywork')