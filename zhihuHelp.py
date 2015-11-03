# -*- coding: utf-8 -*-
# 放置于首位
import sys  # 修改默认编码

reload(sys)
sys.setdefaultencoding('utf-8')  # 设置系统默认编码
sys.setrecursionlimit(100000)  # 为了适应知乎上的长答案，需要专门设下递归深度限制。。。

# 将./codes添加至库目录中
extend_lib_path = r'./codes'
sys.path.append(extend_lib_path)
