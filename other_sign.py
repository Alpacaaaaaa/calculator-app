'''

提供常用其他如希腊字母等符号的输入

问题是可能存在编码问题

在不同电脑上可能出现编码错误

有待测试

'''

import sys
import sympy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Other_sign(QMainWindow):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.UIinit()
        self.sign = ''

    def UIinit(self):
        self.setWindowTitle('更多符号')


        # 创建界面
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.label = QLabel()
        self.label.setText('在此输入所需符号')
        self.label.setAlignment(Qt.AlignLeft)

        self.input = QLineEdit()

        self.rec_label = QLabel()
        self.rec_label.setText('快捷输入:')
        
        self.alpha = QPushButton('α')
        self.alpha.clicked.connect(self.alpha_input)

        self.beta = QPushButton('β')
        self.beta.clicked.connect(self.beta_input)

        self.gamma = QPushButton('γ')
        self.gamma.clicked.connect(self.gamma_input)

        self.theta = QPushButton('θ')
        self.theta.clicked.connect(self.theta_input)

        # 动作按钮
        self.yesbtn = QPushButton('确定')
        self.yesbtn.clicked.connect(self.read)
        self.yesbtn.setDefault(True)
        self.yesbtn.setShortcut('Enter')
        self.nobtn = QPushButton('取消')
        self.nobtn.clicked.connect(self.close)

        self.Layout = QGridLayout(self.centralwidget)
        self.Layout.addWidget(self.rec_label, 0, 1, 1, 4) 
        self.Layout.addWidget(self.alpha, 1, 1, 1, 1)
        self.Layout.addWidget(self.beta, 1, 2, 1, 1)
        self.Layout.addWidget(self.gamma, 1, 3, 1, 1)
        self.Layout.addWidget(self.theta, 1, 4, 1, 1)
        self.Layout.addWidget(self.label, 2, 1, 1, 4)
        self.Layout.addWidget(self.input, 3, 1, 1, 4)
        self.Layout.addWidget(None, 4, 1, 1, 1)
        self.Layout.addWidget(None, 4, 2, 1, 1)
        self.Layout.addWidget(self.yesbtn, 4, 3, 1, 1)
        self.Layout.addWidget(self.nobtn, 4, 4, 1, 1)

        
    def read(self):
        self.sign = self.input.text()
        self.signal.emit('1')
        self.close()

    def sign_output(self):
        return self.sign

    def alpha_input(self):
        self.input.setText('α')

    def beta_input(self):
        self.input.setText('β')


    def gamma_input(self):
        self.input.setText('γ')


    def theta_input(self):
        self.input.setText('θ')



