'''
基本框架 基于stackedWidget创建

通过改变菜单选项可以使stackedWidget组件显示不同的部分

其中函数setup123分别为需要改写的三个窗口

此框架后续还会逐渐完善

2022年2月16日17:22:37
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
        filemenu = QMenu('文件',self)


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

        self.form1  = QWidget()
        self.setup1()
        self.form2  = QWidget()
        self.setup2()
        self.form3  = QWidget()
        self.setup3()

        # 将三个面板，加入stackedWidget
        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form3)


        self.resize(500,500)


    def switch_mode1(self):
        self.stackedWidget.setCurrentIndex(0)


    def switch_mode2(self):
        self.stackedWidget.setCurrentIndex(1)
        

    def switch_mode3(self):
        self.stackedWidget.setCurrentIndex(2)

    '''以下为三个窗口的设置函数，其中为示例，需要进行改写'''

    def setup1(self):
        self.formLayout1 = QHBoxLayout(self.form1)
        self.label1 = QLabel()
        self.label1.setText("1")
        self.label1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout1.addWidget(self.label1)

    def setup2(self):
        self.formLayout2 = QHBoxLayout(self.form2)
        self.label2 = QLabel()
        self.label2.setText("2")
        self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout2.addWidget(self.label2)


    def setup3(self):
        self.formLayout3 = QHBoxLayout(self.form3)
        self.label3 = QLabel()
        self.label3.setText("3")
        self.label3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout3.addWidget(self.label3)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_mainwindow = Frame()
    the_mainwindow.show()
    sys.exit(app.exec_())
