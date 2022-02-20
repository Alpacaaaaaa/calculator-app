'''

方程计算的初始版本

需要自行输入未知数的数量和名称

'''

from turtle import position
import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Formula(QMainWindow):

    def __init__(self, *args, **kwargs):
        
        super().__init__()
        
    def input(self, exp):
        
        self.setWindowTitle("方程设置")
        self.FLayout = QGridLayout()
        self.resize(300, 400)

        self.times = QComboBox()
        self.times.addItems(['一次', '二次', '三次'])
        self.unknown_count = QComboBox()
        self.unknown_count.addItems(['1', '2', '3'])

        self.FLayout.addWidget(self.times, 2, 0, 1 , 3)
        self.FLayout.addWidget(self.unknown_count, 10, 0, 1, 3)
        self.show()

    def solve(self):
        return None