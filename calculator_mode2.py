'''

部分按键有bug

界面优化

'''

from signal import signal
import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QAction, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from formula import *


class calculator_mode2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.UIinit()
        self.restart = False


    def UIinit(self):

        self.setWindowTitle('mode2')

        # 创建界面
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # 设置stackedWidget
        self.stackedwiget = QStackedWidget()
        self.Layout = QVBoxLayout(self.centralwidget)
        self.Layout.addWidget(self.stackedwiget)


        # 设置选项栏
        formula_setting = QAction('方程', self)
        self.formula = Formula()
        formula_setting.triggered.connect(self.formula.input_n)
        self.formula.Signal.connect(self.read_formula) 


        self.toolbar = self.addToolBar('toolbar ')
        self.toolbar.addAction(formula_setting)


        self.form1 = QWidget()
        self.setup1()
        
        
        self.stackedwiget.addWidget(self.form1)
       

        

    def int1(self):
        self.stackedwiget.setCurrentIndex(0)

    def setup1(self):

        self.layout1 = QGridLayout(self.form1)
        self.layout1.setSpacing(10)
        
        #用于显示输入表达式的label
        self.exp=""
        self.label_exp = QLabel(self.exp, self)
        self.layout1.addWidget(self.label_exp, 0, 0, 1, 5)
        self.label_exp.setAlignment(Qt.AlignRight)

        #用于显示计算结果的label
        self.ans = ""
        self.label_ans = QLabel(self)
        self.layout1.addWidget(self.label_ans, 10, 0, 1, 5)
        self.label_ans.setAlignment(Qt.AlignRight)

        self.mem = []

        # 键盘
        self.names = [
             'a', 'b', 'c', 'x', 'y', 'z',
             'arcsin', 'arccos', 'sin', 'cos', 'tan', 'arctan', 
             'lg', 'ln', '(', ')', 'exp','x!',
             '7', '8', '9','|x|', 'CE', 'Bck',
             '4', '5', '6','*','/', '^',
             '1', '2', '3','+', '-', 'sqrt()', 
             'e', 'pi', '0', '.', '=', 'solve']
       
        self.operators = [
            'a', 'b', 'c', 'x', 'y', 'z',
            '(', ')', '7', '8', '9',
            '/', '4', '5', '6', '*', '1', '2', 
            '3', '-', '0', '.', '+', '=','^']
        self.positions = [(i + 30, j) for i in  range(8) for j in range(6)]
        
        # 定义符号常量
        self.sym_const = {'e':sympy.E, 'pi':sympy.pi}
        #利用lambda表达式给出函数对应的句柄，写成字典的形式，方便调用
        self.functions = {'':lambda x:x, 'arccos':lambda x:sympy.acos(x), 'arcsin':lambda x:sympy.asin(x), 'arctan':lambda x:sympy.atan(x), 'sin':lambda x:sympy.sin(x), 'cos':lambda x:sympy.cos(x), 'tan':lambda x:sympy.tan(x), 'lg':lambda x:sympy.log(x,10), 'ln':lambda x:sympy.log(x), 'sqrt()':lambda x:sympy.sqrt(x), 'x!':lambda x:sympy.factorial(x), '|x|':lambda x:sympy.Abs(x), 'exp':lambda x:sympy.exp(x)}
        self.function_label = {'sin':'sin', 'cos':'cos', 'tan':'tan', 'lg':'lg', 'ln':'ln', 'sqrt()':'sqrt', 'x!':'fac', 'arcsin':'arcsin', 'arccos':'arccos', 'arctan':'arctan', '|x|':'abs', 'exp':'exp'}


        for position, name in zip(self.positions, self.names):
            if name == '':
                continue
            button=QPushButton(name,self)
            if name in self.operators:
                button.setShortcut(name)
            
            if name == 'solve':
                button.clicked.connect(self.Solve)
                

            else:
                button.clicked.connect(self.INPUT)
            
            self.layout1.addWidget(button, *position)

    def INPUT(self):
        
        sender = self.sender().text()


        if self.restart:    #如果需要重开，则清除
            
            self.restart=False
            self.exp=""
            self.ans = ""
            self.mem.clear()
        
        if sender == "CE":
            self.restart=True
            self.label_exp.setText("")
            self.label_ans.setText("")
            self.mem.clear()
            return None

        elif sender == "Bck":
            if len(self.mem)>0:
                self.mem.pop()
            self.compute(self.mem)

        else:
            self.mem.append(sender)
            self.compute(self.mem)


    def compute(self, list):
        if not list:
            self.label_exp.setText("")
            self.label_ans.setText("")
            return None
        self.exp = ""
        self.ans = ""
        for sender in list:
            if sender == "solve": 
                continue

            elif sender == "^":
                self.exp = self.exp + "^"
                self.ans = self.ans  + "**"

            elif sender in self.functions.keys():   
                self.exp=self.exp+self.function_label[sender]+'('
                self.ans=self.ans+self.function_label[sender]+'('

            else:
                self.exp = self.exp + sender
                self.ans = self.ans + sender

     #输出结果与格式控制
        self.label_exp.setFont(QFont("Roman Times", *(12,50) if self.restart else (16,75)))
        self.label_exp.setText(self.exp)
        self.label_ans.setFont(QFont("Roman Times", *(16,75) if self.restart else (12,50)))
        self.label_ans.setText(self.ans)

    def Solve(self):
        
        
        # 解一元简单（符号）方程
        if '=' in self.mem: 
            
            self.ans_list = []
            self.formula.input_1(self.exp)

        # 求解表达式
        else: 
            try:
                self.solve_exp = sympy.sympify(self.exp)
                self.solve_exp = sympy.simplify(self.solve_exp)
                self.ans = str(self.solve_exp)
                #输出结果与格式控制
                self.label_ans.setFont(QFont("Roman Times", *(16,75) if self.restart else (12,50)))
                self.label_ans.setText(self.ans)
            except:
                self.illeagal_input_warning()
            self.mem.clear()


    def illeagal_input_warning(self):       
        reply = QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        if (reply == QMessageBox.Ok):
            return None

    def read_formula(self):
        self.ans_list = self.formula.output()
        print(self.ans_list)

        #输出结果与格式控制
        self.label_ans.setFont(QFont("Roman Times", *(16,75) if self.restart else (12,50)))
        self.ans = ''
        for i in range(self.ans_list.__len__()):
            self.ans = self.ans + '    ' + str(self.ans_list[i])
                
        self.label_ans.setText(self.ans)
        self.mem.clear()
        

        

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mode2 = calculator_mode2()
    mode2.show()
    sys.exit(app.exec_())
