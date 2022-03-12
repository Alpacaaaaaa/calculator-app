import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from calculator import *
from calculator_mode2 import *
from figure import *

class Frame(QMainWindow):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.setWindowTitle('多功能计算器')

        # 创建界面
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.Layout = QVBoxLayout(self.centralwidget)

        # 初始化菜单栏
        self.menubar = QMainWindow.menuBar(self)
        filemenu = QMenu('帮助',self)


        modemenu = QMenu('模式',self)
        mode1 = QAction('简单计算模式',self)
        mode2 = QAction('符号计算模式',self)
        mode3 = QAction('图形计算模式',self)
        modemenu.addAction(mode1)
        modemenu.addAction(mode2)
        modemenu.addAction(mode3)
        mode1.triggered.connect(self.switch_mode1)
        mode2.triggered.connect(self.switch_mode2)
        mode3.triggered.connect(self.switch_mode3)


        exit_Act = QAction('退出',self)
        exit_Act.triggered.connect(qApp.quit)

        self.menubar.addMenu(filemenu)
        self.menubar.addMenu(modemenu)
        self.menubar.addAction(exit_Act)

        # 初始化状态栏
        self.statusbar = QMainWindow.statusBar(self)
        self.statusbar.showMessage('Ready')


        # 设置stackedWidget
        self.stackedWidget = QStackedWidget()
        self.Layout.addWidget(self.stackedWidget)

        self.form1 = Calculator()
        self.form2  = calculator_mode2()
        self.form3  = FunctionFigure()

        # 将三个面板，加入stackedWidget
        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form3)


        # self.resize(500,500)


    def switch_mode1(self):
        self.stackedWidget.setCurrentIndex(0)


    def switch_mode2(self):
        self.stackedWidget.setCurrentIndex(1)
        

    def switch_mode3(self):
        self.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_mainwindow = Frame()
    the_mainwindow.show()
    sys.exit(app.exec_())
