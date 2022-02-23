
'''

挖一个不定积分的坑


'''

import sys
import sympy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class in_integral(QMainWindow):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.UIinit()

    def UIinit(self):
        self.setWindowTitle('不定积分')
        # 创建界面
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # 初始化菜单栏
        self.menubar = QMainWindow.menuBar(self)

        modemenu = QMenu('重积分',self)
        mode1 = QAction('一重积分',self)
        mode2 = QAction('二重积分',self)
        mode3 = QAction('三重积分',self)
        modemenu.addAction(mode1)
        modemenu.addAction(mode2)
        modemenu.addAction(mode3)
        mode1.triggered.connect(self.int1)
        mode2.triggered.connect(self.int2)
        mode3.triggered.connect(self.int3)

        self.menubar.addMenu(modemenu)

        # 设置stackedWidget
        self.stackedWidget = QStackedWidget()
        self.Layout = QVBoxLayout(self.centralwidget)
        self.Layout.addWidget(self.stackedWidget)

        self.form1  = QWidget()
        self.setup1()
        self.form2  = QWidget()
        self.setup2()
        self.form3  = QWidget()
        self.setup3()

        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form3)

        self.resize(500,700)
        self.ans = None

    def int1(self):
        self.stackedWidget.setCurrentIndex(0)

    def int2(self):
        self.stackedWidget.setCurrentIndex(1)

    def int3(self):
        self.stackedWidget.setCurrentIndex(2)

    def setup1(self):
        preview = QPushButton("预览")
        confirm = QPushButton("确认")


        self.uboundEdit = QLineEdit()
        self.lboundEdit = QLineEdit()
        self.funcEdit = QTextEdit()
        self.grid1 = QGridLayout(self.form1)
        self.grid1.setSpacing(20)
        self.grid1.addWidget(preview)
        self.grid1.addWidget(confirm)

    def setup2(self):
        preview = QPushButton("预览")
        confirm = QPushButton("确认")


        self.uboundEdit = QLineEdit()
        self.lboundEdit = QLineEdit()
        self.funcEdit = QTextEdit()
        self.grid2= QGridLayout(self.form2)
        self.grid2.setSpacing(20)
        self.grid2.addWidget(preview)
        self.grid2.addWidget(confirm)

    def setup3(self):
        preview = QPushButton("预览")
        confirm = QPushButton("确认")


        self.uboundEdit = QLineEdit()
        self.lboundEdit = QLineEdit()
        self.funcEdit = QTextEdit()
        self.grid3 = QGridLayout(self.form3)
        self.grid3.setSpacing(20)
        self.grid3.addWidget(preview)
        self.grid3.addWidget(confirm)

    