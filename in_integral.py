
'''

目前可计算一重不定积分

输出结果未渲染

'''

from symtable import Symbol
import sys
import sympy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class In_integral(QMainWindow):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.exp = ""
        self.x = sympy.Symbol("x")
        self.out = ""
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

        self.resize(400,300)
        self.ans = None

    def int1(self):
        self.stackedWidget.setCurrentIndex(0)

    def int2(self):
        self.stackedWidget.setCurrentIndex(1)

    def int3(self):
        self.stackedWidget.setCurrentIndex(2)

    def setup1(self):
        cal = QPushButton("计算")
        preview = QPushButton("预览")
        cal.clicked.connect(self.calu)
        
        self.funcEdit = QTextEdit()
        self.funcEdit.setText(self.exp)
        self.xEditlabel = QLabel()
        self.xEditlabel.setText("输入积分变量:默认为x")
        self.xEdit = QTextEdit()
        self.result = QLabel()
        self.result.setText("None")
        self.grid1 = QGridLayout(self.form1)
        self.grid1.setSpacing(20)
        self.grid1.addWidget(self.funcEdit)
        self.grid1.addWidget(self.xEditlabel)
        self.grid1.addWidget(self.xEdit)
        self.grid1.addWidget(cal)
        self.grid1.addWidget(self.result)
        self.grid1.addWidget(preview)

    def setup2(self):
        return None

    def setup3(self):
        return None

    def calu(self):
        try:
            self.exp = self.funcEdit.toPlainText()
            tempx = self.xEdit.toPlainText()
            print(tempx)
            if tempx != '':
                self.x = sympy.sympify(tempx)
            self.exp = sympy.sympify(self.exp)
            self.out = sympy.Integral(self.exp, self.x)
            self.result.setText(str(self.out.doit()))
        except:
            self.error()

    
    def error(self):
        reply = QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        self.exp = ''
        self.ans = ''
        if (reply == QMessageBox.Ok):
            return None
