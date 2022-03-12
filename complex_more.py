'''

对于带符号复数，需要判断符号变量的是实数还是复数。
先默认为实数。

'''


import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class complex_more(QMainWindow):
    Signal = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        
        super().__init__()
        self.exp = []
        self.ans = []
        self.UIinit()

    def UIinit(self):
        self.setWindowTitle("复数")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        
        self.Layout = QGridLayout(self.centralwidget)

        self.initlabel = QLabel()
        self.initlabel.setFont(QFont("Roman Times", *(16,75)))

        self.resultlabel = QLabel()
        self.resultlabel.setFont(QFont("Roman Times", *(16,75)))

        self.ampbtn = QPushButton('幅度')
        self.ampbtn.clicked.connect(self.amp)
        self.argbtn = QPushButton('相位')
        self.argbtn.clicked.connect(self.arg)
        self.rebtn = QPushButton('实部')
        self.rebtn.clicked.connect(self.re)
        self.imbtn = QPushButton('虚部')
        self.imbtn.clicked.connect(self.im)
        self.nobtn = QPushButton('退出')
        self.nobtn.clicked.connect(self.exit)
        self.nobtn.setDefault(True)

        self.Layout.addWidget(self.initlabel, 1, 1, 1, 4)
        self.Layout.addWidget(self.resultlabel, 2, 1, 1, 4)
        self.Layout.addWidget(self.ampbtn, 3, 1, 1, 1)
        self.Layout.addWidget(self.argbtn, 3, 2, 1, 1)
        self.Layout.addWidget(self.rebtn, 3, 3, 1, 1)
        self.Layout.addWidget(self.imbtn, 3, 4, 1, 1)

        self.Layout.addWidget(self.nobtn, 4, 4, 1, 1)

    def input(self, exp):
        try:
            self.exp = exp
            self.initlabel.setText(str(self.exp))
        except:
            self.error()

    def amp(self):
        try:
            self.ans = sympy.Abs(self.exp)
            self.resultlabel.setText(str(self.ans))
            return
        except:
            self.error()

    def arg(self):
        try:
            self.ans = sympy.arg(self.exp)
            self.resultlabel.setText(str(self.ans))
            return
        except:
            self.error()

    def re(self):
        try:
            self.ans = sympy.re(self.exp)
            self.resultlabel.setText(str(self.ans))
            return
        except:
            self.error()

    def im(self):
        try:
            self.ans = sympy.im(self.exp)
            self.resultlabel.setText(str(self.ans))
            return
        except:
            self.error()
    
    def exit(self):
        self.Signal.emit(1)
        self.close()

    def error(self):
        reply = QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        self.exp = ''
        self.ans = ''
        if (reply == QMessageBox.Ok):
            return None
        
