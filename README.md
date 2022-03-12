
#  calculator app
当前main分支主要合并了mode1数值计算部分，主要的文件是calculator.py（其中定义Calculator类），solver.py（其中定义solver类），MATRICES.py（其中定义mat_Calculator类）。我觉得可以先合并一下calculator.py，这部分已经比较稳定了。

合并时calculator.py只需要在主界面文件中加入```from calculator import Calculator```，并且把calculator.py文件中148行```self.show()```注释掉在主界面中构造一个Calculator对象并嵌入到stackedwidget的页面中就行。

主要问题是，Calculator对象自带一个工具栏，主界面应该会有一个工具栏，这两个怎么调。

main分支已合并mode2符号计算已完成部分。目前可实现：普通计算， 符号表达式化简， 直接求解一元（含符号）方程， 求解一重不定积分。

