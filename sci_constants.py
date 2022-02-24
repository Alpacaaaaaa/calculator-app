'''
调用科学常数弹窗的实现
'''
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QMenu, QAction, QLineEdit, QTextEdit, QGridLayout, QStackedWidget, QPushButton, QMainWindow)
from PyQt5 import QtSvg, QtCore
import sympy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget
from str2svg import tex2svg
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem
from str2svg import tex2svg

em_constants = {'μN': '5.05078353e-27', 'μB': '9.27400968e-24', 'e': '1.602176565e-19', 'Φ0': '2.067833758e-15', 'G0': '7.748091735e-5', 'KJ': '4.8359878e14', 'RK': '2.58128074e4'}
em_annotations = {'μN': '核磁矩，J/T', 'μB': '玻尔磁子，J/T', 'e': '元电荷，C', 'Φ0': '磁通量量子，Wb', 'G0': '电导量子，S', 'KJ': '约瑟夫森常量，Hz/V', 'RK': '克里青常量，Ω'}
em_latex = {'μN': '\mu_N', 'μB': '\mu_B', 'e': 'e', 'Φ0': '\Phi_0', 'G0': 'G_0', 'KJ': 'K_J', 'RK': 'R_K'}

pc_constants = {'u': '1.660538921e-27', 'F': '9.64853365e4', 'NA': '6.02214129e23', 'k': '1.3806488e-23', 'Vm': '2.2710953e-2', 'R': '8.3144621', 'c1': '3.74177153e-16', 'c2': '1.438777e-1', 'σ':'5.670373e-6'}
pc_annotations = {'u': '原子质量单位，kg', 'F': '法拉第常量，C/mol', 'NA': '阿伏伽德罗常量，1/mol', 'k': '玻尔兹曼常量，J/K', 'Vm': '气体摩尔体积，m^3/mol', 'R': '普适气体常数，J/(mol*K)', 'c1': '第一辐射常量，W/m^2', 'c2': '第二辐射常量，m*K', 'σ':'斯特藩-玻尔兹曼常量，W/(m^2*K^4)'}
pc_latex = {'u': 'u', 'F': 'F', 'NA': 'N_A', 'k': 'k', 'Vm': 'V_m', 'R': 'R', 'c1': 'c_1', 'c2': 'c_2', 'σ':'\sigma'}

un_constants = {'h': '6.62606957e-34', 'c': '2.99792458e8', 'ε0': '8.854187817e-12', 'μ0': '1.256637061e-6', 'Z0':'3.767303135e2', 'G':'6.67384e-11', 'lp': '1.616199e-35', 'tp': '5.39106e-44', 'α': '7.29735257e-3'}
un_annotations = {'h': '普朗克常量，J*s', 'c': '真空光速，m/s', 'ε0': '真空介电常数，F/m', 'μ0': '真空磁导率，N/A^2', 'Z0':'真空阻抗特性，Ω', 'G':'万有引力常量，N*m^2/kg^2', 'lp': '普朗克长度，m', 'tp': '普朗克时间，s', 'α': '精细结构常数，1'}
un_latex = {'h': 'h', 'c': 'c', 'ε0': '\\varepsilon_0', 'μ0': '\mu_0', 'Z0':'Z_0', 'G':'G', 'lp': 'l_p', 'tp': 't_p', 'α': '\\alpha'}

class const(QMainWindow):
    Signal = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('调用科学常数')

        # 创建界面
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # 初始化菜单栏
        self.menubar = QMainWindow.menuBar(self)

        modemenu = QMenu('切换类别',self)
        mode1 = QAction('电磁常数',self)
        mode2 = QAction('通用常数',self)
        mode3 = QAction('物理化学常数',self)
        modemenu.addAction(mode2)
        modemenu.addAction(mode1)
        modemenu.addAction(mode3)
        mode1.triggered.connect(self.int1)
        mode2.triggered.connect(self.int2)
        mode3.triggered.connect(self.int3)

        self.menubar.addMenu(modemenu)

        # 设置stackedWidget
        self.stackedWidget = QStackedWidget()
        self.Layout = QVBoxLayout(self.centralwidget)
        self.Layout.addWidget(self.stackedWidget)

        self.form2  = QWidget()
        self.setup2()

        self.form1  = QWidget()
        self.setup1()

        self.form3  = QWidget()
        self.setup3()

        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form3)

        self.resize(500,300)

    def int1(self):
        self.stackedWidget.setCurrentIndex(0)

    def int2(self):
        self.stackedWidget.setCurrentIndex(1)

    def int3(self):
        self.stackedWidget.setCurrentIndex(2)

    def setup1(self):
        self.grid1 = QGridLayout(self.form1)

        self.form1.listwidget_1 = QListWidget(self.form1)  #实例化列表控件
        self.form1.listwidget_1.setFixedWidth(100)

        for c in em_constants.keys():  
            self.form1.item = QListWidgetItem(c)  #把字符串转化为QListWidgetItem项目对象
            self.form1.listwidget_1.addItem(self.form1.item)  #添加项目

        self.grid1.addWidget(self.form1.listwidget_1,0,0,6,1)

        self.label1 = QLabel('参数')
        self.grid1.addWidget(self.label1,0,1,1,2)
        self.label1.setFont(QFont("Roman Times", 12, 75))

        self.label11 = QLabel('')
        self.grid1.addWidget(self.label11,1,1,1,2)
        self.label11.setFont(QFont("Roman Times", 10, 50))

        self.form1.listwidget_1.itemClicked.connect(self.clicked1)  #单击列表控件时发出信号

        self.svgWidget1 = QtSvg.QSvgWidget()
        self.grid1.addWidget(self.svgWidget1, 2, 1, 4, 2, QtCore.Qt.AlignCenter)

    def setup2(self):
        self.grid2 = QGridLayout(self.form2)

        self.form2.listwidget_1 = QListWidget(self.form2)  #实例化列表控件
        self.form2.listwidget_1.setFixedWidth(100)

        for c in un_constants.keys():  
            self.form2.item = QListWidgetItem(c)  #把字符串转化为QListWidgetItem项目对象
            self.form2.listwidget_1.addItem(self.form2.item)  #添加项目

        self.grid2.addWidget(self.form2.listwidget_1,0,0,6,1)

        self.label2 = QLabel('参数')
        self.grid2.addWidget(self.label2,0,1,1,2)
        self.label2.setFont(QFont("Roman Times", 12, 75))

        self.label21 = QLabel('')
        self.grid2.addWidget(self.label21,1,1,1,2)
        self.label21.setFont(QFont("Roman Times", 10, 50))

        self.form2.listwidget_1.itemClicked.connect(self.clicked2)  #单击列表控件时发出信号

        self.svgWidget2 = QtSvg.QSvgWidget()
        self.grid2.addWidget(self.svgWidget2, 2, 1, 4, 2, QtCore.Qt.AlignCenter)

    def setup3(self):
        self.grid3 = QGridLayout(self.form3)

        self.form3.listwidget_1 = QListWidget(self.form3)  #实例化列表控件
        self.form3.listwidget_1.setFixedWidth(100)

        for c in pc_constants.keys():  
            self.form3.item = QListWidgetItem(c)  #把字符串转化为QListWidgetItem项目对象
            self.form3.listwidget_1.addItem(self.form3.item)  #添加项目

        self.grid3.addWidget(self.form3.listwidget_1,0,0,6,1)

        self.label3 = QLabel('参数')
        self.grid3.addWidget(self.label3,0,1,1,2)
        self.label3.setFont(QFont("Roman Times", 12, 75))

        self.label31 = QLabel('')
        self.grid3.addWidget(self.label31,1,1,1,2)
        self.label31.setFont(QFont("Roman Times", 10, 50))

        self.form3.listwidget_1.itemClicked.connect(self.clicked3)  #单击列表控件时发出信号

        self.svgWidget3 = QtSvg.QSvgWidget()
        self.grid3.addWidget(self.svgWidget3, 2, 1, 4, 2, QtCore.Qt.AlignCenter)

    def clicked1(self):
        self.label1.setText(em_annotations[self.form1.listwidget_1.currentItem().text()].split('，')[0])
        self.label11.setText('量纲：' + em_annotations[self.form1.listwidget_1.currentItem().text()].split('，')[1])
        latex_code = em_latex[self.form1.listwidget_1.currentItem().text()] + '=' + em_constants[self.form1.listwidget_1.currentItem().text()].replace('e','\\times 10^{') +'}'
        self.svgWidget1.load(tex2svg(latex_code))
        self.svgWidget1.setFixedSize(10*len(latex_code),35)
        self.grid1.addWidget(self.svgWidget1, 2, 1, 4, 2, QtCore.Qt.AlignCenter)

    def clicked2(self):
        self.label2.setText(un_annotations[self.form2.listwidget_1.currentItem().text()].split('，')[0])
        self.label21.setText('量纲：' + un_annotations[self.form2.listwidget_1.currentItem().text()].split('，')[1])
        latex_code = un_latex[self.form2.listwidget_1.currentItem().text()] + '=' + un_constants[self.form2.listwidget_1.currentItem().text()].replace('e','\\times 10^{') +'}'
        self.svgWidget2.load(tex2svg(latex_code))
        self.svgWidget2.setFixedSize(10*len(latex_code) if len(latex_code)<33 else 330,35)
        self.grid2.addWidget(self.svgWidget2, 2, 1, 4, 2, QtCore.Qt.AlignCenter)
    
    def clicked3(self):
        self.label3.setText(pc_annotations[self.form3.listwidget_1.currentItem().text()].split('，')[0])
        self.label31.setText('量纲：' + pc_annotations[self.form3.listwidget_1.currentItem().text()].split('，')[1])
        latex_code = pc_latex[self.form3.listwidget_1.currentItem().text()] + '=' + pc_constants[self.form3.listwidget_1.currentItem().text()].replace('e','\\times 10^{') +'}'
        self.svgWidget3.load(tex2svg(latex_code))
        self.svgWidget3.setFixedSize(10*len(latex_code),35)
        self.grid3.addWidget(self.svgWidget3, 2, 1, 4, 2, QtCore.Qt.AlignCenter)
    
    def Conf(self):
        return None