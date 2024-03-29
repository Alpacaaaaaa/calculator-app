'''
数值结算主界面实现
最近更新：修复连按三下小数点导致的异常；更改默认插入数字的值；添加连续两个表达式异常处理
'''
import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QAction, QMainWindow, QFrame
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from SETTINGS import SETTINGS
from integral import IntFrame
from limit import lim
from series import series
from sci_constants import const
from config import *

class expression(): #表达式类，用来计算一个形如(a ± b */ c ^ d)的表达式的值。
    def __init__(self):
        self.res=sympy.Integer(0)  #当前表达式中已经计算完了的部分，对应上面的a
        self.prev_sym=""    #对应a、b之间的那个±.表示正在运算的部分应当被加到res中还是从res中减去.
        self.prev_num=None  #对应b，被乘/除数
        self.curr_num=None  #对应c或d，正在读入的数
        self.base_num=None  #对应c，底数
        self.curr_sym=""    #对应b、c之间的*/.表示b、c相乘还是相除
        self.curr_num_text=""   #用来读取数值型的curr_num的中间变量
    def Eprint(self):
        print("[{0},{1},{2},{3}]".format(self.res,self.prev_num,self.base_num,self.curr_num))
#利用栈结构来处理括号嵌套.每遇到'('就把当前的expression对象入栈，在栈顶新开一个expression对象处理当前的括号.每遇到')'就出栈，处理上一级括号
#栈初始化
EXP=expression()
CAL=[]
CAL.append(EXP)

#同样利用栈结构来处理函数调用.开一个函数栈来记录每层括号()外面对应的是什么函数
FUNC=[]


#GUI界面
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.restart=True   #restart标志量表示是否重开

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(3)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(245,245,245))
        self.setPalette(self.palette)

        #工具栏选项
        #“设置”选项卡
        settings = QAction('设置', self)
        settings.triggered.connect(self.show_option)
        #“积分”选项卡
        dint_input = QAction('定积分', self)
        dint_input.triggered.connect(self.integral_input)
        #“极限”选项卡
        lim_input = QAction("极限",self)
        lim_input.triggered.connect(self.lim_input)
        #“级数和”选项卡
        serie_input = QAction("级数和",self)
        serie_input.triggered.connect(self.serie_input)
        #“调用”选项卡
        const_input = QAction("科学常数",self)
        const_input.triggered.connect(self.const_input)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(settings)
        self.toolbar.addAction(dint_input)
        self.toolbar.addAction(lim_input)
        self.toolbar.addAction(serie_input)
        self.toolbar.addAction(const_input)

        #初始化“设置”“积分”“极限”“级数和”选项卡
        self.setting_dialog = SETTINGS()
        self.int_dialog = IntFrame()
        self.int_dialog.Signal.connect(self.read_integral)
        self.lim_dialog = lim()
        self.lim_dialog.Signal.connect(self.read_lim)
        self.serie_dialog = series()
        self.serie_dialog.Signal.connect(self.read_serie)
        self.const_dialog = const()
        self.const_dialog.Signal.connect(self.read_const)

        self.names = ['arcsin', 'arccos', 'arctan', 'sin', 'cos', 'tan', 'lg', 'ln', 'x!', '|x|', 'exp', 'sqrt()', '^', '(', ')', 'CE', 'Bck', '/', '7', '8', '9', '*10^(', '*', '4', '5', '6', 'e', '-', '1', '2', '3', 'pi', '+', 'Ans', '0', '.', '=']
        self.operators = ['(', ')', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '+', '=','^']

        #定义常量e与pi
        self.constants = {'e':sympy.E, 'pi':sympy.pi}

        #利用lambda表达式给出函数对应的句柄，写成字典的形式，方便调用
        self.functions = {'':lambda x:x, 'arccos':lambda x:sympy.acos(x), 'arcsin':lambda x:sympy.asin(x), 'arctan':lambda x:sympy.atan(x), 'sin':lambda x:sympy.sin(x), 'cos':lambda x:sympy.cos(x), 'tan':lambda x:sympy.tan(x), 'lg':lambda x:sympy.log(x,10), 'ln':lambda x:sympy.log(x), 'sqrt()':lambda x:sympy.sqrt(x), 'x!':lambda x:sympy.factorial(x), '|x|':lambda x:sympy.Abs(x), 'exp':lambda x:sympy.exp(x)}
        self.function_label = {'sin':'sin', 'cos':'cos', 'tan':'tan', 'lg':'lg', 'ln':'ln', 'sqrt()':'sqrt', 'x!':'fac', 'arcsin':'arcsin', 'arccos':'arccos', 'arctan':'arctan', '|x|':'abs', 'exp':'exp'}

        tri_grid = QGridLayout()
        tri_grid.setSpacing(3)
        for i in range(12):
            btn = QPushButton(self.names[i])
            btn.clicked.connect(self.INPUT)
            btn.setStyleSheet(style_sheet_func)
            btn.pressed.connect(self.pressed_color)
            btn.released.connect(self.released_color)
            tri_grid.addWidget(btn,i//6,i%6)
            btn.setFixedHeight(55)
        grid.addLayout(tri_grid,19,0,1,5)
        positions = [(i+20,j) for i in range(5) for j in range(5)]
        
        for position, name in zip(positions, self.names[12:]):   #对每个button设置位置、文字与快捷键
            button=QPushButton(name,self)
            if name in self.operators:
                button.setShortcut(name)
            if name == 'Bck':
                button.setShortcut('backspace')

            button.clicked.connect(self.INPUT)
            button.setFixedSize(90,60)
            button.setStyleSheet(style_sheet_digit if name.isdigit() else style_sheet)
            grid.addWidget(button, *position)
            button.pressed.connect(self.pressed_color)
            button.released.connect(self.released_color)

        #用于显示输入表达式的label
        self.exp=""
        self.label_exp = QLabel(self.exp, self)
        grid.addWidget(self.label_exp, 0, 0, 1, 5)
        self.label_exp.setAlignment(Qt.AlignRight|Qt.AlignBottom)
        self.label_exp.setFixedHeight(72)

        #用于显示计算结果的label
        self.label_ans = QLabel(self)
        grid.addWidget(self.label_ans, 10, 0, 1, 5)
        self.label_ans.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.label_ans.setFixedHeight(72)

        self.mem = []
        self.ans = 0

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        self.move(300, 150)
        self.setWindowTitle('Calculator')

    #button被按下事件处理函数
    def INPUT(self):
        global CAL

        if self.restart:    #如果需要重开，则清除CAL栈
            self.clear_mem()
        
        sender=self.sender().text() #判断按下了哪个button
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

    def compute(self,list): #传入一个list对象——也就是self.mem，根据这个list对象解析出有效的表达式并计算
        if not list:
            self.label_exp.setText("")
            self.label_ans.setText("")
            return None
        self.exp=""
        CAL.clear()
        FUNC.clear()
        EXP=expression()
        CAL.append(EXP)
        error_flag = False

        placeholder = ['flag', '_)']    #定义占位符列表.相比于一个有效的计算表达式，一个只输入了一半的表达式缺少了1.结尾处若干个匹配的右括号2.结尾的'='.因此，这里把这些缺少的都补上，这样就可以让输入一半的表达式变有效
        if list[-1]!='=':
            for i in range(list.count('(')-list.count(')')):
                list.append('_)')       #'_)'对应右括号，这里把括号全部匹配
            list.append('flag')         #'flag'对应'='

        for sender in list:
            if sender == '*10^(':
                self.exp = self.exp + sender
                if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                    try:
                        CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else sympy.Integer(0)
                    except:
                        error_flag = True
                        break
                    if CAL[-1].curr_num == Ellipsis:                        #额外排除一下Ellipsis类型
                        error_flag = True
                        break
                    
                if (CAL[-1].base_num!=None):                                #再结算^运算
                    CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                    CAL[-1].base_num=None

                if CAL[-1].prev_num==None:
                    CAL[-1].prev_num=CAL[-1].curr_num

                else:
                    if (CAL[-1].curr_sym=="*"):
                        CAL[-1].prev_num=CAL[-1].prev_num*CAL[-1].curr_num
                    elif (CAL[-1].curr_sym=="/"):
                        try:
                            CAL[-1].prev_num=CAL[-1].prev_num/CAL[-1].curr_num
                        except:
                            error_flag = True
                CAL[-1].curr_sym='*'
                CAL[-1].base_num=sympy.Integer(10)
                CAL[-1].curr_num_text=""
                temp=expression()
                CAL.append(temp)
                FUNC.append("")

            elif sender in self.constants.keys():   #按下的是pi或e等常量
                if CAL[-1].curr_num or CAL[-1].curr_num_text:
                    error_flag = True

                CAL[-1].curr_num=self.constants[sender]
                self.exp+=sender

            elif sender == 'Ans':
                CAL[-1].curr_num=self.ans
                self.exp+=sender

            elif sender in self.functions.keys():   #遇到函数
                temp=expression()           #新开一个expression对象压入CAL栈
                CAL.append(temp)            
                FUNC.append(sender)         #将函数记录到函数栈里面
                self.exp=self.exp+self.function_label[sender]+'('

            elif sender in self.operators or sender in placeholder:  #如果按下的是运算符
                if not(sender in placeholder):
                    self.exp=self.exp+sender
                self.restart=False

                if sender=="(":    #新开一个expression类压入CAL栈,同时函数栈压入空字符串
                    temp=expression()
                    CAL.append(temp)
                    FUNC.append("")

                elif sender.isdigit() or sender == '.': #如果是数字或小数点，继续读
                    if CAL[-1].curr_num:
                        error_flag = True
                    else:
                        CAL[-1].curr_num_text+=sender

                elif (sender=="+" or sender=="-" or sender==")" or sender=="=" or sender in placeholder):    #遇到+-)=，进行计算
                    if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                        try:
                            CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else (sympy.Integer(1) if (CAL[-1].base_num!=None or CAL[-1].curr_sym=='*' or CAL[-1].curr_sym=='/') else sympy.Integer(0))
                        except:
                            error_flag = True
                            break
                        if CAL[-1].curr_num == Ellipsis:                        #额外排除一下Ellipsis类型
                            error_flag = True
                            break

                    if (CAL[-1].base_num!=None):                                #再结算^运算
                        CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                        CAL[-1].base_num=None

                    sgn=-1 if (CAL[-1].prev_sym=="-") else 1

                    if (CAL[-1].curr_sym==""):                                  #再结算*/运算
                        CAL[-1].res+=CAL[-1].curr_num*sgn

                    elif (CAL[-1].curr_sym=="*"):
                        CAL[-1].res=CAL[-1].res+sgn*CAL[-1].curr_num*CAL[-1].prev_num

                    elif (CAL[-1].curr_sym=="/"):
                        try:
                            CAL[-1].res=CAL[-1].res+sgn*CAL[-1].prev_num/CAL[-1].curr_num
                        except:
                            error_flag = True
                    CAL[-1].prev_sym=sender
                    CAL[-1].curr_sym=""
                    CAL[-1].prev_num=CAL[-1].curr_num=None
                    CAL[-1].curr_num_text=""

                    if sender == "=":
                        self.restart=True
                        self.ans = CAL[0].res
                    elif sender ==")" or sender == '_)':
                        if len(CAL)>1:
                            ans=CAL[-1].res
                            CAL.pop()
                            if CAL[-1].curr_num != None:
                                error_flag = True
                            CAL[-1].curr_num=self.functions[FUNC[-1]](ans)
                            FUNC.pop()

                elif (sender=="*" or sender=="/"):  #遇到*/，记录在prev_sym和prev_num中
                    if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                        try:
                            CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else sympy.Integer(1)
                        except:
                            error_flag = True
                            break
                        if CAL[-1].curr_num == Ellipsis:                        #额外排除一下Ellipsis类型
                            error_flag = True
                            break
                    
                    if (CAL[-1].base_num!=None):                                #再结算^运算
                        CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                        CAL[-1].base_num=None

                    if CAL[-1].prev_num==None:
                        CAL[-1].prev_num=CAL[-1].curr_num

                    else:
                        if (CAL[-1].curr_sym=="*"):
                            CAL[-1].prev_num=CAL[-1].prev_num*CAL[-1].curr_num
                        elif (CAL[-1].curr_sym=="/"):
                            try:
                                CAL[-1].prev_num=CAL[-1].prev_num/CAL[-1].curr_num
                            except:
                                error_flag = True
                    CAL[-1].curr_sym=sender
                    CAL[-1].curr_num=None
                    CAL[-1].curr_num_text=""

                elif (sender=="^"): #遇到^，
                    if (CAL[-1].curr_num==None):                                #先结算curr_num的读取
                        try:
                            CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else sympy.Integer(1)
                        except:
                            error_flag = True
                        if CAL[-1].curr_num == Ellipsis:                        #额外排除一下Ellipsis类型
                            error_flag = True
                            break
                    if (CAL[-1].base_num!=None):                                #再结算^运算
                        CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                
                    CAL[-1].base_num=CAL[-1].curr_num
                    CAL[-1].curr_num=None
                    CAL[-1].curr_num_text=""
            elif type(sender)!=type(''):
                if CAL[-1].curr_num or CAL[-1].curr_num_text:
                    error_flag = True
                if type(sender)==tuple: #元组，对应输入的是科学常量
                    name, num = sender
                    CAL[-1].curr_num = sympy.sympify(num)
                    self.exp = self.exp + name
                else:                   #积分、极限、求和等
                    CAL[-1].curr_num = sender
                    self.exp = self.exp + '(...)'

        #输出结果与格式控制
        self.label_exp.setFont(QFont("Calibri Light", *(12,50) if self.restart else (16,75)))
        self.label_exp.setText(self.exp)
        self.label_ans.setFont(QFont("Calibri Light", *(16,75) if self.restart else (12,50)))
        if error_flag or CAL[0].res.has(sympy.nan):
            self.label_ans.setText("错误")
        elif CAL[0].res.has(sympy.oo,sympy.zoo):
            self.label_ans.setText("无穷")
        else:
            self.label_ans.setText("{0}".format(CAL[0].res.evalf(self.setting_dialog.dig) if (not self.setting_dialog.sym)  else CAL[0].res))
        while list[-1] in placeholder:
            list.pop()   

    def pressed_color(self):    #按下button时改变颜色
        self.sender().setStyleSheet(style_sheet_released)

    def released_color(self):   #松开时恢复
        self.sender().setStyleSheet(style_sheet_digit if self.sender().text().isdigit() else style_sheet)

    def show_option(self):
        self.setting_dialog.show()
    def integral_input(self):
        self.int_dialog.show()
    def read_integral(self):
        if self.restart:    #如果需要重开，则清除CAL栈
            self.clear_mem()
        self.mem.append(self.int_dialog.ans)
        self.compute(self.mem)
    def lim_input(self):
        self.lim_dialog.show()
    def read_lim(self):
        if self.restart:    #如果需要重开，则清除CAL栈
            self.clear_mem()
        self.mem.append(self.lim_dialog.ans)
        self.compute(self.mem)
    def serie_input(self):
        self.serie_dialog.show()
    def read_serie(self):
        if self.restart:    #如果需要重开，则清除CAL栈
            self.clear_mem()
        self.mem.append(self.serie_dialog.ans)
        self.compute(self.mem)
    def const_input(self):
        self.const_dialog.show()
    def read_const(self):
        if self.restart:    #如果需要重开，则清除CAL栈
            self.clear_mem()
        self.mem.append(self.const_dialog.ans)
        self.compute(self.mem)
    def clear_mem(self):
        CAL.clear()
        FUNC.clear()
        EXP=expression()
        CAL.append(EXP)
        self.restart=False
        self.exp=""
        self.mem.clear()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Calculator()
    sys.exit(app.exec_())