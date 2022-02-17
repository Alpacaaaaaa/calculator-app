'''
尝试加入函数运算.
现存问题：
"设置"选项卡里面角度/弧度转换选项还没有实现，然后反三角函数输出格式(符号/小数)也有点小问题，以及'Bck'键不可用，以及没法抛异常，输入奇怪的东西会崩掉
'''
import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QAction, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon
from SETTINGS import SETTINGS

class expression(): #表达式类，用来计算一个形如(a ± b */ c ^ d)的表达式的值。
    def __init__(self):
        self.res=0  #当前表达式中已经计算完了的部分，对应上面的a
        self.prev_sym=""    #对应a、b之间的那个±.表示正在运算的部分应当被加到res中还是从res中减去.
        self.prev_num=None  #对应b，被乘/除数
        self.curr_num=None  #对应c或d，正在读入的数
        self.base_num=None  #对应c，底数
        self.curr_sym=""    #对应b、c之间的*/.表示b、c相乘还是相除
        self.curr_num_text=""   #用来读取数值型的curr_num的中间变量
    def Eprint(self):
        print("[{0},{1},{2},{3}]".format(self.res,self.prev_num,self.base_num,self.curr_num))
#利用栈结构来处理括号嵌套.每遇到'('就把当前的expression对象入栈，在栈顶新开一个expression对象处理当前的括号.每遇到')'就出栈，处理上一级括号
#初始化
EXP=expression()
CAL=[]
CAL.append(EXP)

#同样利用栈结构来处理函数调用.开一个函数栈来记录每层括号()外面对应的是什么函数
FUNC=[]

#异常处理函数，待完善
def ERROR_INPUT():
    return None


#GUI界面
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.restart=True   #restart标志量表示是否重开

    def initUI(self):
        grid = QGridLayout()

        #工具栏选项
        #“设置”选项卡
        settings = QAction('设置', self)
        # settings.setShortcut('Alt+S')
        settings.triggered.connect(self.show_option)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(settings)

        # self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Calculator Simple')    
        # self.show()

        #初始化“设置”选项卡
        self.setting_dialog=SETTINGS()

        self.names = ['arcsin', 'arccos', 'sin', 'cos', 'tan', 'arctan', 'lg', 'ln', '(', ')', 'x^y', 'CE', 'Bck', '^', '/', 'sqrt()', '7', '8', '9', '*', 'x!', '4', '5', '6', '-', '|x|', '1', '2', '3', '+', 'e', 'pi', '0', '.', '=']
        self.operators = ['(', ')', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '+', '=','^']

        #定义常量e与pi，有小数和符号两种类型，self.constants根据self.setting_dialog.sym来判断指向符号类型的还是小数类型的
        self.sym_const = {'e':sympy.E, 'pi':sympy.pi}
        self.num_const = {'e':2.718281828459, 'pi':3.141592653589}
        self.constants = self.sym_const if self.setting_dialog.sym else self.num_const

        #利用lambda表达式给出函数对应的句柄，写成字典的形式，方便调用
        self.functions = {'':lambda x:x, 'arccos':lambda x:sympy.acos(x), 'arcsin':lambda x:sympy.asin(x), 'arctan':lambda x:sympy.atan(x), 'sin':lambda x:sympy.sin(x), 'cos':lambda x:sympy.cos(x), 'tan':lambda x:sympy.tan(x), 'lg':lambda x:sympy.log(x,10), 'ln':lambda x:sympy.log(x), 'sqrt()':lambda x:sympy.sqrt(x), 'x!':lambda x:sympy.factorial(x), '|x|':lambda x:sympy.Abs(x)}
        self.function_label = {'sin':'sin', 'cos':'cos', 'tan':'tan', 'lg':'lg', 'ln':'ln', 'sqrt()':'sqrt', 'x!':'fac', 'arcsin':'arcsin', 'arccos':'arccos', 'arctan':'arctan'}

        positions = [(i+20,j) for i in range(7) for j in range(5)]
        
        for position, name in zip(positions, self.names):   #对每个button设置位置、文字与快捷键
            if name == '':
                continue
            button=QPushButton(name,self)
            if name in self.operators:
                button.setShortcut(name)
            
            button.clicked.connect(self.INPUT)
            grid.addWidget(button, *position)

        #用于显示输入表达式的label
        self.exp=""
        self.label_exp = QLabel(self.exp, self)
        grid.addWidget(self.label_exp, 0, 0, 1, 5)
        self.label_exp.setAlignment(Qt.AlignRight)

        #用于显示计算结果的label
        self.label_ans = QLabel(self)
        grid.addWidget(self.label_ans, 10, 0, 1, 5)
        self.label_ans.setAlignment(Qt.AlignRight)

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()

    #button被按下事件处理函数
    def INPUT(self):
        global CAL

        self.constants = self.sym_const if self.setting_dialog.sym else self.num_const
        if self.restart:    #如果需要重开，则清除CAL栈
            CAL.clear()
            EXP=expression()
            CAL.append(EXP)
            self.restart=False
            self.exp=""
        
        sender=self.sender().text() #判断按下了哪个button
        if sender == "CE":
            self.restart=True
            self.label_exp.setText("")
            self.label_ans.setText("")
            return None

        elif sender in self.constants.keys():   #按下的是pi或e等常量
            CAL[-1].curr_num=self.constants[sender]
            self.exp+=sender

        elif sender in self.functions.keys():   #遇到函数
            temp=expression()           #新开一个expression对象压入CAL栈
            CAL.append(temp)            
            FUNC.append(sender)         #将函数记录到函数栈里面
            self.exp=self.exp+self.function_label[sender]+'('

        elif sender in self.operators:  #如果按下的是运算符
            self.exp=self.exp+sender
            self.restart=False

            if sender=="(":    #新开一个expression类压入CAL栈,同时函数栈压入空字符串
                temp=expression()
                CAL.append(temp)
                FUNC.append("")

            elif sender.isdigit() or sender == '.': #如果是数字或小数点，继续读
                CAL[-1].curr_num_text+=sender

            elif (sender=="+" or sender=="-" or sender==")" or sender=="="):    #遇到+-)=，进行计算
                # print(CAL[-1].curr_num)
                if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                    CAL[-1].curr_num=float(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else 0

                if (CAL[-1].base_num!=None):                                #再结算^运算
                    CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                    CAL[-1].base_num=None

                sgn=-1 if (CAL[-1].prev_sym=="-") else 1

                if (CAL[-1].curr_sym==""):                                  #再结算*/运算
                    CAL[-1].res+=CAL[-1].curr_num*sgn

                elif (CAL[-1].curr_sym=="*"):
                    CAL[-1].res=CAL[-1].res+sgn*CAL[-1].curr_num*CAL[-1].prev_num

                elif (CAL[-1].curr_sym=="/"):
                    CAL[-1].res=CAL[-1].res+sgn*CAL[-1].prev_num/CAL[-1].curr_num

                CAL[-1].prev_sym=sender
                CAL[-1].curr_sym=""
                CAL[-1].prev_num=CAL[-1].curr_num=None
                CAL[-1].curr_num_text=""

                if sender == "=":
                    self.restart=True
                elif sender ==")":
                    ans=CAL[-1].res
                    CAL.pop()
                    CAL[-1].curr_num=self.functions[FUNC[-1]](ans)
                    FUNC.pop()

            elif (sender=="*" or sender=="/"):  #遇到*/，记录在prev_sym和prev_num中
                if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                    CAL[-1].curr_num=float(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else 0
                
                if (CAL[-1].base_num!=None):                                #再结算^运算
                    CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                    CAL[-1].base_num=None

                if CAL[-1].prev_num==None:
                    CAL[-1].prev_num=CAL[-1].curr_num

                else:
                    if (CAL[-1].curr_sym=="*"):
                        CAL[-1].prev_num=CAL[-1].prev_num*CAL[-1].curr_num
                    elif (CAL[-1].curr_sym=="/"):
                        CAL[-1].prev_num=CAL[-1].prev_num/CAL[-1].curr_num
                CAL[-1].curr_sym=sender
                CAL[-1].curr_num=None
                CAL[-1].curr_num_text=""

            elif (sender=="^"): #遇到^，
                if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                    CAL[-1].curr_num=float(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else 0
                if (CAL[-1].base_num!=None):                                #再结算^运算
                    CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
            
                CAL[-1].base_num=CAL[-1].curr_num
                CAL[-1].curr_num=None
                CAL[-1].curr_num_text=""
                
            
        #输出结果与格式控制
        self.label_exp.setFont(QFont("Roman Times", *(12,50) if self.restart else (16,75)))
        self.label_exp.setText(self.exp)
        self.label_ans.setFont(QFont("Roman Times", *(16,75) if self.restart else (12,50)))
        self.label_ans.setText("{0}".format(CAL[0].res))
        

    def show_option(self):
        self.setting_dialog.show()
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec_())
