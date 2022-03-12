'''

可以直接在显示区输入等式以快速进行一元方程求解

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
    Signal = pyqtSignal(int)
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
    

    # 界面设置（一元函数情况）
    def setup1(self):
        
        self.Layout1 = QGridLayout(self.form1)
        # 输入ui
        self.unknown_name_label_1 = QLabel()
        self.unknown_name_label_1.setText('输入未知数名称:')
        self.unknown_name_label_1.setAlignment(Qt.AlignLeft)
        self.unknown_name_1 = QLineEdit()
        self.unknown_name_1.setPlaceholderText('输入未知数(例如:x)')
        self.unknown_name_1.setFocus(True)
        
        # 动作按钮
        self.yesbtn_1 = QPushButton('确定')
        self.yesbtn_1.clicked.connect(self.solve_1)
        self.yesbtn_1.setDefault(True)
        self.yesbtn_1.setShortcut('Enter')
        self.nobtn_1 = QPushButton('取消')
        self.nobtn_1.clicked.connect(self.close)
        # 布局
        self.Layout1.addWidget(self.unknown_name_label_1, 1, 0, 1, 2)
        self.Layout1.addWidget(self.unknown_name_1, 2, 0, 1, 2)
        self.Layout1.addWidget(self.yesbtn_1, 3, 0, 1, 1)
        self.Layout1.addWidget(self.nobtn_1, 3, 1, 1, 1)

    # 界面设置（多元函数情况）
    def setupn(self):
        
        self.Layoutn = QGridLayout(self.formn)

        self.substack = QStackedWidget()
        
        # 输入ui
        self.count_label = QLabel()
        self.count_label.setText('输入方程个数:(超过3个请使用矩阵运算)')
        self.count_label.setAlignment(Qt.AlignLeft)
        self.count_input = QComboBox()
        self.count_input.addItems(['1', '2', '3'])
        self.count_input.currentIndexChanged[int].connect(self.switch)
      

        self.subform1 = QWidget()
        self.subset1()
        self.subform2 = QWidget()
        self.subset2()
        self.subform3 = QWidget()
        self.subset3()
        self.substack.addWidget(self.subform1)
        self.substack.addWidget(self.subform2)
        self.substack.addWidget(self.subform3)

        # 动作按钮
        self.yesbtn = QPushButton('确定')
        self.yesbtn.clicked.connect(self.solve_n)
        self.yesbtn.setDefault(True)
        self.yesbtn.setShortcut('Enter')
        self.nobtn = QPushButton('取消')
        self.nobtn.clicked.connect(self.close)

        # 布局
        self.Layoutn.setSpacing(10)
        self.Layoutn.addWidget(self.count_label, 1, 1, 1, 2)
        self.Layoutn.addWidget(self.count_input, 2, 1, 1, 2)
        self.Layoutn.addWidget(self.substack, 3, 1, 1, 2)
        self.Layoutn.addWidget(self.yesbtn, 6, 1, 1, 1)
        self.Layoutn.addWidget(self.nobtn, 6, 2, 1, 1)
        

    def subset1(self):
        self.sublayout1 = QVBoxLayout(self.subform1)
        self.subformula_label_1_1 = QLabel()
        self.subformula_label_1_1.setText('请输入方程:')
        self.subform_input_1_1 = QLineEdit()
        self.subform_input_1_1.setPlaceholderText('输入完整等式(如x=1)')
        
        self.unknown_name_label_1_1 = QLabel()
        self.unknown_name_label_1_1.setText('输入未知数名称:')
        self.unknown_name_label_1_1.setAlignment(Qt.AlignLeft)
        self.unknown_name_1_1 = QLineEdit()
        self.unknown_name_1_1.setPlaceholderText('(例如:x)')
        
        self.sublayout1.addWidget(self.subformula_label_1_1)
        self.sublayout1.addWidget(self.subform_input_1_1)
        self.sublayout1.addWidget(self.unknown_name_label_1_1)
        self.sublayout1.addWidget(self.unknown_name_1_1)
        self.sublayout1.addStretch(1)


    def subset2(self):
        self.sublayout2 = QVBoxLayout(self.subform2)
        self.subformula_label_2_1 = QLabel()
        self.subformula_label_2_1.setText('请输入方程:')
        self.subform_input_2_1 = QLineEdit()
        self.subform_input_2_1.setPlaceholderText('输入完整等式(如x=1)')
        self.subformula_label_2_2 = QLabel()
        self.subformula_label_2_2.setText('请输入方程:')
        self.subform_input_2_2 = QLineEdit()
        self.subform_input_2_2.setPlaceholderText('输入完整等式(如x=1)')
              
        self.unknown_name_label_2_1 = QLabel()
        self.unknown_name_label_2_1.setText('输入未知数1名称:')
        self.unknown_name_label_2_1.setAlignment(Qt.AlignLeft)
        self.unknown_name_2_1 = QLineEdit()
        self.unknown_name_2_1.setPlaceholderText('(例如:x)')
        self.unknown_name_label_2_2 = QLabel()
        self.unknown_name_label_2_2.setText('输入未知数2名称:')
        self.unknown_name_label_2_2.setAlignment(Qt.AlignLeft)
        self.unknown_name_2_2 = QLineEdit()
        self.unknown_name_2_2.setPlaceholderText('(例如:x)')
        
        self.sublayout2.addWidget(self.subformula_label_2_1)
        self.sublayout2.addWidget(self.subform_input_2_1)
        self.sublayout2.addWidget(self.subformula_label_2_2)
        self.sublayout2.addWidget(self.subform_input_2_2)
        self.sublayout2.addWidget(self.unknown_name_label_2_1)
        self.sublayout2.addWidget(self.unknown_name_2_1)
        self.sublayout2.addWidget(self.unknown_name_label_2_2)
        self.sublayout2.addWidget(self.unknown_name_2_2)
        self.sublayout2.addStretch(1)

    
    def subset3(self):
        self.sublayout3 = QVBoxLayout(self.subform3)
        self.subformula_label_3_1 = QLabel()
        self.subformula_label_3_1.setText('请输入方程:')
        self.subform_input_3_1 = QLineEdit()
        self.subform_input_3_1.setPlaceholderText('输入完整等式(如x=1)')
        self.subformula_label_3_2 = QLabel()
        self.subformula_label_3_2.setText('请输入方程:')
        self.subform_input_3_2 = QLineEdit()
        self.subform_input_3_2.setPlaceholderText('输入完整等式(如x=1)')
        self.subformula_label_3_3 = QLabel()
        self.subformula_label_3_3.setText('请输入方程:')
        self.subform_input_3_3 = QLineEdit()
        self.subform_input_3_3.setPlaceholderText('输入完整等式(如x=1)')
        
        self.unknown_name_label_3_1 = QLabel()
        self.unknown_name_label_3_1.setText('输入未知数1名称:')
        self.unknown_name_label_3_1.setAlignment(Qt.AlignLeft)
        self.unknown_name_3_1 = QLineEdit()
        self.unknown_name_3_1.setPlaceholderText('(例如:x)')
        self.unknown_name_label_3_2 = QLabel()
        self.unknown_name_label_3_2.setText('输入未知数2名称:')
        self.unknown_name_label_3_2.setAlignment(Qt.AlignLeft)
        self.unknown_name_3_2 = QLineEdit()
        self.unknown_name_3_2.setPlaceholderText('(例如:x)')
        self.unknown_name_label_3_3 = QLabel()
        self.unknown_name_label_3_3.setText('输入未知数3名称:')
        self.unknown_name_label_3_3.setAlignment(Qt.AlignLeft)
        self.unknown_name_3_3 = QLineEdit()
        self.unknown_name_3_3.setPlaceholderText('(例如:x)')
        
        self.sublayout3.addWidget(self.subformula_label_3_1)
        self.sublayout3.addWidget(self.subform_input_3_1)
        self.sublayout3.addWidget(self.subformula_label_3_2)
        self.sublayout3.addWidget(self.subform_input_3_2)
        self.sublayout3.addWidget(self.subformula_label_3_3)
        self.sublayout3.addWidget(self.subform_input_3_3)
        self.sublayout3.addWidget(self.unknown_name_label_3_1)
        self.sublayout3.addWidget(self.unknown_name_3_1)
        self.sublayout3.addWidget(self.unknown_name_label_3_2)
        self.sublayout3.addWidget(self.unknown_name_3_2)
        self.sublayout3.addWidget(self.unknown_name_label_3_3)
        self.sublayout3.addWidget(self.unknown_name_3_3)


    def switch(self, count):
        self.count = 0
        self.substack.setCurrentIndex(count)
        self.count = count + 1
    

    def input_1(self, exp):
        self.exp = exp
        self.stackedwidget.setCurrentIndex(0)
        self.show()


    def input_n(self):
        self.stackedwidget.setCurrentIndex(1)
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
            
        self.Signal.emit(1)
        self.close()
    

    def solve_n(self):

        return None

    
    def output(self):
        return self.ans 


    # 异常处理函数
    def formula_error(self):
        reply = QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        self.ans = ''
        if (reply == QMessageBox.Ok):
            return None
