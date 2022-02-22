'''

可以直接在显示区输入等式以快速进行一元方程求解

多元方程施工中

'''

from posixpath import split
from re import S, T
from symtable import Symbol
from turtle import position
import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Formula(QMainWindow):
    Signal = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        
        super().__init__()
        self.UIinit()
        
        
    def UIinit(self):
        
        self.exp = []
        self.ans = []
        self.setWindowTitle("方程设置")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.stackedwidget = QStackedWidget()
        self.Layout = QVBoxLayout(self.centralwidget)
        self.Layout.addWidget(self.stackedwidget)

        self.form1 = QWidget()
        self.setup1()
        self.stackedwidget.addWidget(self.form1)
        self.formn = QWidget()
        self.setupn()
        self.stackedwidget.addWidget(self.formn)
        
        self.resize(300, 200)


    def switch(self, index):
        if index == 1:
            self.stackedwidget.setCurrentIndex(0)

        elif index == 2:
            self.stackedwidget.setCurrentIndex(1)
    

    # 界面设置（一元函数情况）
    def setup1(self):
        
        self.Layout1 = QGridLayout(self.form1)

        self.unknown_name_label_1 = QLabel()
        self.unknown_name_label_1.setText('输入未知数名称：')
        self.unknown_name_label_1.setAlignment(Qt.AlignLeft)
        self.unknown_name_1 = QLineEdit()
        self.unknown_name_1.setPlaceholderText('输入未知数(例如:x)')
        self.unknown_name_1.setFocus(True)
        self.yesbtn = QPushButton('确定')
        self.yesbtn.clicked.connect(self.solve_1)

        self.yesbtn.setDefault(True)
        self.yesbtn.setShortcut('Enter')
        self.nobtn = QPushButton('取消')
        self.nobtn.clicked.connect(self.close)

        self.Layout1.addWidget(self.unknown_name_label_1, 1, 0, 1, 2)
        self.Layout1.addWidget(self.unknown_name_1, 2, 0, 1, 2)
        self.Layout1.addWidget(self.yesbtn, 3, 0, 1, 1)
        self.Layout1.addWidget(self.nobtn, 3, 1, 1, 1)

    # 界面设置（多元函数情况）
    def setupn(self):
        
        self.Layoutn = QGridLayout(self.formn)

        self.substack = QStackedWidget()
        
        self.subform = []
        

        self.count_label = QLabel()
        self.count_label.setText('输入方程个数:')
        self.count_label.setAlignment(Qt.AlignLeft)
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText('输入方程个数')
        


        self.unknown_name_label = QLabel()
        self.unknown_name_label.setText('输入未知数名称:')
        self.unknown_name_label.setAlignment(Qt.AlignLeft)
        self.unknown_name = QLineEdit()
        self.unknown_name.setPlaceholderText('输入未知数(例如:x)')


        self.Layoutn.setSpacing(10)
        self.Layoutn.addWidget(self.count_label)
        self.Layoutn.addWidget(self.count_input)
        self.Layoutn.addWidget(self.substack)
        self.Layoutn.addWidget(self.unknown_name_label)
        self.Layoutn.addWidget(self.unknown_name)
        self.Layoutn.addWidget(self.yesbtn)
        self.Layoutn.addWidget(self.nobtn)
        

    def input_1(self, exp):
        self.exp = exp
        self.stackedwidget.setCurrentIndex(0)
        self.show()

    def input_n(self):
        self.stackedwidget.setCurrentIndex(1)
        self.count = self.count_input.text()
        self.show()
        return

    def solve_1(self):
        
        self.exp1 = 0
        self.exp2 = 0
        self.unknown = 'x'

        try:
            self.exp1 = sympy.sympify(self.exp.split('=', 1)[0])
            self.exp2 = sympy.sympify(self.exp.split('=', 1)[1])
        

            self.formula = self.exp1 - self.exp2
            self.unknown = self.unknown_name_1.text()
            self.x = sympy.Symbol(self.unknown)

            self.ans = sympy.solve(self.formula, self.x)
        
        except:
            self.formula_error()
            
        self.Signal.emit('1')
        self.close()

    
    
    def formula_error(self):
        reply = QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        if (reply == QMessageBox.Ok):
            return None


    def solve_n(self):
        self.count = int(self.count)
        return None

    
    def output(self):
        return self.ans
