
import sys
import sympy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QAction, QMessageBox, QMainWindow, QLineEdit, QTextEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from config import *

#GUI界面
class FunctionFigure(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.restart=True   #restart标志量表示是否重开
        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(245,245,245))
        self.setPalette(self.palette)

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(3)

        self.names = ['arcsin', 'arccos', 'sin', 'cos', 'tan', 'arctan', 'lg', 'ln', '(', ')', 
        'exp', 'CE', 'Bck', '**', '/', 'sqrt()', '7', '8', '9', '*', 'x!', '4', '5', '6', '-', 
        '|x|', '1', '2', '3', '+', 'e', 'pi', '0', '.', 'x']
        self.operators = ['(', ')', '/','*', '-', '+','**','x']
        self.numbers = ['1', '2', '3','4', '5', '6', '7', '8', '9','0','.']

        #定义常量e与pi
        self.constants = {'e':sympy.E, 'pi':sympy.pi}

        #利用lambda表达式给出函数对应的句柄，写成字典的形式，方便调用
        self.functions = {'arccos':'acos', 'arcsin':'asin', 'arctan':'atan',
        'sin':'sin', 'cos':'cos', 'tan':'tan', 'lg':'1/log(10)*log', 
        'ln':'log', 'sqrt()':'sqrt', 'x!':'factorial', '|x|':'Abs',
         'exp':'exp'}
        self.function_label = {'sin':'sin', 'cos':'cos', 
        'tan':'tan', 'lg':'lg', 'ln':'ln', 
        'sqrt()':'sqrt', 'x!':'fac', 
        'arcsin':'arcsin', 'arccos':'arccos', 
        'arctan':'arctan', '|x|':'abs', 'exp':'exp'}

        positions = [(i + 2, j ) for i in range(7) for j in range(5)]
        
        for position, name in zip(positions, self.names):   #对每个button设置位置、文字与快捷键
            if name == '':
                continue
            button = QPushButton(name, self)
            button.setFocusPolicy(QtCore.Qt.NoFocus)
            button.setStyleSheet(style_sheet_digit if name.isdigit() else style_sheet)
            button.clicked.connect(self.input)
            button.setFixedSize(90,60)
            grid.addWidget(button, *position)
            button.released.connect(self.released_color)
            button.pressed.connect(self.pressed_color)

        self.msgbox = QMessageBox()

        btn_grid = QGridLayout()
        label1 = QLabel("输入函数")
        label1.setAlignment(QtCore.Qt.AlignCenter)
        btn_grid.addWidget(label1,0,0)

        self.func=""
        self.func_to_caculate=""
        self.func_exp = QLineEdit()
        btn_grid.addWidget(self.func_exp,0,1,1,4)
        grid.addLayout(btn_grid,0,0,1,5)

        lineedit_grid = QGridLayout()

        label2 = QLabel("区间起始点")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        lineedit_grid.addWidget(label2, 0, 0)

        self.start=""
        self.start_exp = QLineEdit()
        lineedit_grid.addWidget(self.start_exp, 0, 1)

        button_plot = QPushButton('plot', self)
        button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        button_plot.clicked.connect(self.input)
        button_plot.setFixedSize(75,30)
        lineedit_grid.addWidget(button_plot, 0, 2)


        label3 = QLabel("区间终止点")
        label3.setAlignment(QtCore.Qt.AlignCenter)
        lineedit_grid.addWidget(label3, 0, 3)

        self.stop=""
        self.stop_exp = QLineEdit()
        lineedit_grid.addWidget(self.stop_exp, 0, 4)

        grid.addLayout(lineedit_grid,1,0,1,5)

        rowSize = 25
        colSize = 25
        for row in range(grid.rowCount()):
            grid.setRowStretch(row, 1)
            grid.setRowMinimumHeight(row, rowSize)
        for col in range(grid.columnCount()):
            grid.setColumnStretch(col, 1)
            grid.setColumnMinimumWidth(col, colSize)

        self.mem_func=[]
        self.mem_num_start=[]
        self.mem_num_stop=[]

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        self.move(300, 150)
        self.setWindowTitle('Function figure')

    # button被按下事件处理函数
    def input(self):
        sender=self.sender().text()
        if sender == "plot":
            self.printfigure(self.func_to_caculate, self.start, self.stop)
        LineEDIT = QApplication.focusWidget()
        if LineEDIT in [self.func_exp]:      #最好再判断下选中的是不是QLineEdit控件
            self.input_func()
        elif LineEDIT in [self.start_exp]:
            self.input_start()
        elif LineEDIT in [self.stop_exp]:
            self.input_stop()
    
    def input_func(self):    
        if self.restart:    #如果需要重开，则清除CAL栈
            self.restart=False
            self.func=""
            self.func_to_caculate=""
            self.mem_func.clear()
       
        sender=self.sender().text() #判断按下了哪个button
        if sender == "CE":
            self.restart=True
            self.func_exp.setText("")
            self.mem_func.clear()
            return None

        elif sender == "Bck":
            if len(self.mem_func)>0:
                self.mem_func.pop()
            self.print_func(self.mem_func)
        else:
            self.mem_func.append(sender)
            self.print_func(self.mem_func)

    def print_func(self, list): #传入一个list对象——也就是self.mem，根据这个list对象解析出有效的表达式并计算
        if not list:
            self.func_exp.setText("")
            return None
        
        self.func=""
        self.func_to_caculate=""

        for sender in list:
            if sender in self.constants.keys():   #按下的是pi或e等常量
                self.func += sender
                self.func_to_caculate += sender

            elif sender in self.function_label.keys():   #遇到函数
                self.func += self.function_label[sender]+'('
                self.func_to_caculate += self.functions[sender]+'('

            elif sender in self.operators or sender in self.numbers:  #如果按下的是运算符
                self.func += sender
                self.func_to_caculate += sender

        #输出结果与格式控制
        self.func_exp.setFont(QFont("Roman Times", *(6,25) if self.restart else (8,35)))
        self.func_exp.setText(self.func)

    def input_start(self):    
        if self.restart:    #如果需要重开，则清除CAL栈
            self.restart=False
            self.start=""
            self.mem_num_start.clear()
       
        sender=self.sender().text() #判断按下了哪个button
        if sender == "CE":
            self.restart=True
            self.start_exp.setText("")
            self.mem_num_start.clear()
            return None

        elif sender == "Bck":
            if len(self.mem_num_start)>0:
                self.mem_num_start.pop()
            self.print_start(self.mem_num_start)
        else:
            self.mem_num_start.append(sender)
            self.print_start(self.mem_num_start)

    def print_start(self, list): #传入一个list对象——也就是self.mem，根据这个list对象解析出有效的表达式并计算
        if not list:
            self.start_exp.setText("")
            return None
        
        self.start=""

        for sender in list:
            if sender in self.constants.keys():   #按下的是pi或e等常量
                self.start += sender

            elif sender in self.operators or sender in self.numbers:  #如果按下的是运算符
                self.start += sender

        #输出结果与格式控制
        self.start_exp.setFont(QFont("Roman Times", *(6,25) if self.restart else (8,35)))
        self.start_exp.setText(self.start)  

    def input_stop(self):    
        if self.restart:    #如果需要重开，则清除CAL栈
            self.restart=False
            self.stop=""
            self.mem_num_stop.clear()
       
        sender=self.sender().text() #判断按下了哪个button
        if sender == "CE":
            self.restart=True
            self.stop_exp.setText("")
            self.mem_num_stop.clear()
            return None

        elif sender == "Bck":
            if len(self.mem_num_stop)>0:
                self.mem_num_stop.pop()
            self.print_stop(self.mem_num_stop)
        else:
            self.mem_num_stop.append(sender)
            self.print_stop(self.mem_num_stop)

    def print_stop(self, list): #传入一个list对象——也就是self.mem，根据这个list对象解析出有效的表达式并计算
        if not list:
            self.stop_exp.setText("")
            return None
        
        self.stop=""

        for sender in list:
            if sender in self.constants.keys():   #按下的是pi或e等常量
                self.stop += sender

            elif sender in self.operators or sender in self.numbers:  #如果按下的是运算符
                self.stop += sender

        #输出结果与格式控制
        self.stop_exp.setFont(QFont("Roman Times", *(6,25) if self.restart else(8,35)))
        self.stop_exp.setText(self.stop)

    def printfigure(self, func_str, start_str, stop_str):
        try:
            function = sympy.sympify(func_str)
        except:
            self.msgbox.setText("输入公式有误!")
            self.msgbox.exec()
            return None
        
        try:
            numstart = float(sympy.sympify(start_str))
        except:
            self.msgbox.setText("输入数字有误!")
            self.msgbox.exec()
            return None
        
        try:
            numstop = float(sympy.sympify(stop_str))
        except:
            self.msgbox.setText("输入数字有误!")
            self.msgbox.exec()
            return None
        
        if numstop < numstart:
            self.msgbox.setText("输入区间有误!")
            self.msgbox.exec()
            return None
        else:
            try:
                x = sympy.Symbol('x')
                sympy.plot(function, (x, numstart, numstop))
            except:
                self.msgbox.setText("输入公式或区间有误!")
                self.msgbox.exec()
                return None
    def pressed_color(self):    #按下button时改变颜色
        self.sender().setStyleSheet(style_sheet_released)

    def released_color(self):   #松开时恢复
        self.sender().setStyleSheet(style_sheet_digit if self.sender().text().isdigit() else style_sheet)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = FunctionFigure()
    sys.exit(app.exec_())