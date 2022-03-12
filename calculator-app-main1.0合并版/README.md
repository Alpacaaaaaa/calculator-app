
#  已有内容
当前main分支主要合并了mode1数值计算部分，主要的文件是calculator.py（其中定义Calculator类），solver.py（其中定义solver类），MATRICES.py（其中定义mat_Calculator类）。我觉得可以先合并一下calculator.py，这部分已经比较稳定了。

合并时calculator.py只需要在主界面文件中加入```from calculator import Calculator```，并且把calculator.py文件中148行```self.show()```注释掉在主界面中构造一个Calculator对象并嵌入到stackedwidget的页面中就行。

主要问题是，Calculator对象自带一个工具栏，主界面应该会有一个工具栏，这两个怎么调。

main分支已合并mode2符号计算已完成部分。目前可实现：普通计算， 符号表达式化简， 直接求解一元（含符号）方程， 求解一重不定积分。

另外，已添加mode3，能绘制数学函数在某一区间内的图像。

## 关于出现问题

- 首先是工具栏冲突的问题，我的方法是保留对Qmainwindow的继承属性，主界面避免使用工具栏，而是使用菜单栏。目前的问题是，似乎有点丑。

- 另外，因为三个图形界面并不是按照统一格式写的，所以ui很丑。

## 关于目前发现的小bug

### mode1：

- 空白情况下连按3个小数点会报错。``` TypeError: unsupported operand type(s) for *: 'ellipsis' and 'int' ```

### mode2：

- lg没有用

### mode3：

- 当对0取10为底对数时不报错

先修改ui，我下午进一步找bug和写文档。
