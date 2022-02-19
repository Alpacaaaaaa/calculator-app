'''
输入定积分弹窗的实现
现存问题：对不合法表达式抛异常；三重积分积分顺序；界面太丑了！！！svg图大小
'''
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QMenu, QAction, QLineEdit, QTextEdit, QGridLayout, QApplication, QStackedWidget, QPushButton, QMainWindow)
from PyQt5 import QtSvg
import sympy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget
from io import BytesIO
import matplotlib.pyplot as plt

class IntFrame(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('插入定积分')

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
        preview.clicked.connect(self.Render)
        confirm.clicked.connect(self.Conf)

        ubound = QLabel('积分上限')
        lbound = QLabel('积分下限')
        func = QLabel('被积函数')

        self.uboundEdit = QLineEdit()
        self.lboundEdit = QLineEdit()
        self.funcEdit = QTextEdit()
        self.grid1 = QGridLayout(self.form1)
        self.grid1.setSpacing(20)

        self.grid1.addWidget(ubound, 0, 0)
        self.grid1.addWidget(self.uboundEdit, 0, 1)

        self.grid1.addWidget(lbound,1, 0)
        self.grid1.addWidget(self.lboundEdit, 1, 1)

        self.grid1.addWidget(func, 2, 0)
        self.grid1.addWidget(self.funcEdit, 2, 1, 2, 1)        

        self.svgWidget1 = QtSvg.QSvgWidget()
        self.grid1.addWidget(self.svgWidget1,4,0,5,1)

        self.grid1.addWidget(preview, 9, 0)
        self.grid1.addWidget(confirm, 9, 1)

    def setup2(self):
        preview = QPushButton("预览")
        confirm = QPushButton("确认")
        preview.clicked.connect(self.Render)
        confirm.clicked.connect(self.Conf)

        ubound = QLabel('变量x积分上限')
        lbound = QLabel('变量x积分下限')
        ubound2 = QLabel('变量y积分上限')
        lbound2 = QLabel('变量y积分下限')
        func = QLabel('被积函数')

        self.uboundEdit21 = QLineEdit()
        self.lboundEdit21 = QLineEdit()
        self.uboundEdit22 = QLineEdit()
        self.lboundEdit22 = QLineEdit()
        self.funcEdit2 = QTextEdit()
        self.grid2 = QGridLayout(self.form2)
        self.grid2.setSpacing(20)

        self.grid2.addWidget(ubound, 0, 0)
        self.grid2.addWidget(self.uboundEdit21, 0, 1)

        self.grid2.addWidget(lbound,1, 0)
        self.grid2.addWidget(self.lboundEdit21, 1, 1)

        self.grid2.addWidget(ubound2, 2, 0)
        self.grid2.addWidget(self.uboundEdit22, 2, 1)

        self.grid2.addWidget(lbound2, 3, 0)
        self.grid2.addWidget(self.lboundEdit22, 3, 1)

        self.grid2.addWidget(func, 4, 0)
        self.grid2.addWidget(self.funcEdit2, 4, 1, 2, 1)        

        self.svgWidget2 = QtSvg.QSvgWidget()
        self.grid2.addWidget(self.svgWidget2,6,0,5,1)

        self.grid2.addWidget(preview, 11, 0)
        self.grid2.addWidget(confirm, 11, 1)

    def setup3(self):
        preview = QPushButton("预览")
        confirm = QPushButton("确认")
        preview.clicked.connect(self.Render)
        confirm.clicked.connect(self.Conf)

        ubound = QLabel('变量x积分上限')
        lbound = QLabel('变量x积分下限')
        ubound2 = QLabel('变量y积分上限')
        lbound2 = QLabel('变量y积分下限')
        ubound3 = QLabel('变量z积分上限')
        lbound3 = QLabel('变量z积分下限')
        func = QLabel('被积函数')

        self.uboundEdit31 = QLineEdit()
        self.lboundEdit31 = QLineEdit()
        self.uboundEdit32 = QLineEdit()
        self.lboundEdit32 = QLineEdit()
        self.uboundEdit33 = QLineEdit()
        self.lboundEdit33 = QLineEdit()
        self.funcEdit3 = QTextEdit()
        self.grid3 = QGridLayout(self.form3)
        self.grid3.setSpacing(15)

        self.grid3.addWidget(ubound, 0, 0)
        self.grid3.addWidget(self.uboundEdit31, 0, 1)

        self.grid3.addWidget(lbound,1, 0)
        self.grid3.addWidget(self.lboundEdit31, 1, 1)

        self.grid3.addWidget(ubound2, 2, 0)
        self.grid3.addWidget(self.uboundEdit32, 2, 1)

        self.grid3.addWidget(lbound2, 3, 0)
        self.grid3.addWidget(self.lboundEdit32, 3, 1)

        self.grid3.addWidget(ubound3, 4, 0)
        self.grid3.addWidget(self.uboundEdit33, 4, 1)

        self.grid3.addWidget(lbound3, 5, 0)
        self.grid3.addWidget(self.lboundEdit33, 5, 1)

        self.grid3.addWidget(func, 6, 0)
        self.grid3.addWidget(self.funcEdit3, 6, 1, 2, 1)        

        self.svgWidget3 = QtSvg.QSvgWidget()
        self.grid3.addWidget(self.svgWidget3, 8, 0, 5, 1)

        self.grid3.addWidget(preview, 13, 0)
        self.grid3.addWidget(confirm, 13, 1)

        self.setGeometry(300, 300, 350, 500)
        self.setWindowTitle('输入定积分')    

    def Render(self):
        if self.stackedWidget.currentIndex() == 0:
            upperbound = sympy.latex(sympy.sympify(self.uboundEdit.text())) if self.uboundEdit.text().strip() else ''
            lowerbound = sympy.latex(sympy.sympify(self.lboundEdit.text())) if self.lboundEdit.text().strip() else ''
            f = sympy.latex(sympy.sympify(self.funcEdit.toPlainText())) if self.funcEdit.toPlainText().strip() else ''
            latex_code = r'\int_{'+lowerbound+'}^{'+upperbound+'}'+f+'\mathrm{d}x'
            self.svgWidget1.load(tex2svg(latex_code,1))
            self.grid1.addWidget(self.svgWidget1,4,0,5,2)
            self.svgWidget1.show()
            self.svgWidget1.setFixedHeight(40)

        elif self.stackedWidget.currentIndex() == 1:
            upperbound = sympy.latex(sympy.sympify(self.uboundEdit21.text())) if self.uboundEdit21.text().strip() else ''
            lowerbound = sympy.latex(sympy.sympify(self.lboundEdit21.text())) if self.lboundEdit21.text().strip() else ''
            f = sympy.latex(sympy.sympify(self.funcEdit2.toPlainText())) if self.funcEdit2.toPlainText().strip() else ''
            upperbound2 = sympy.latex(sympy.sympify(self.uboundEdit22.text())) if self.uboundEdit22.text().strip() else ''
            lowerbound2 = sympy.latex(sympy.sympify(self.lboundEdit22.text())) if self.lboundEdit22.text().strip() else ''
            latex_code = r'\iint_{'+lowerbound+'\leq x\leq '+upperbound+';'+lowerbound2+'\leq y\leq '+upperbound2+'}'+f+'\mathrm{d}x\mathrm{d}y'
            self.svgWidget2.load(tex2svg(latex_code,1))
            self.grid2.addWidget(self.svgWidget2,6,0,5,2)
            self.svgWidget2.show()
            self.svgWidget2.setFixedHeight(40)

        else:
            upperbound = sympy.latex(sympy.sympify(self.uboundEdit31.text())) if self.uboundEdit31.text().strip() else ''
            lowerbound = sympy.latex(sympy.sympify(self.lboundEdit31.text())) if self.lboundEdit31.text().strip() else ''
            f = sympy.latex(sympy.sympify(self.funcEdit3.toPlainText())) if self.funcEdit3.toPlainText().strip() else ''
            upperbound2 = sympy.latex(sympy.sympify(self.uboundEdit32.text())) if self.uboundEdit32.text().strip() else ''
            lowerbound2 = sympy.latex(sympy.sympify(self.lboundEdit32.text())) if self.lboundEdit32.text().strip() else ''
            upperbound3 = sympy.latex(sympy.sympify(self.uboundEdit33.text())) if self.uboundEdit33.text().strip() else ''
            lowerbound3 = sympy.latex(sympy.sympify(self.lboundEdit33.text())) if self.lboundEdit33.text().strip() else ''
            latex_code = r'\iiint_{'+lowerbound+'\leq x\leq '+upperbound+';'+lowerbound2+'\leq y\leq '+upperbound2+';'+lowerbound3+'\leq z\leq '+upperbound3+'}'+f+'\mathrm{d}x\mathrm{d}y\mathrm{d}z'
            self.svgWidget3.load(tex2svg(latex_code,1))
            self.grid3.addWidget(self.svgWidget3,8,0,5,2)
            self.svgWidget3.show()
            self.svgWidget3.setFixedHeight(40)
    
    def Conf(self):
        if self.stackedWidget.currentIndex()==0:
            upperbound = sympy.sympify(self.uboundEdit.text()) if self.uboundEdit.text().strip() else ''
            lowerbound = sympy.sympify(self.lboundEdit.text()) if self.lboundEdit.text().strip() else ''
            f = sympy.sympify(self.funcEdit.toPlainText()) if self.funcEdit.toPlainText().strip() else ''
            self.latex_code=r'\int_{'+sympy.latex(lowerbound)+'}^{'+sympy.latex(upperbound)+'}'+sympy.latex(f)+'\mathrm{d}x'
            x = sympy.Symbol('x')
            self.ans=sympy.integrate(f, (x, lowerbound, upperbound))
        elif self.stackedWidget.currentIndex()==1:
            exchange = 'y' in self.uboundEdit21.text() or 'y' in self.lboundEdit21.text()
            upperbound = sympy.sympify(self.uboundEdit21.text()) if self.uboundEdit21.text().strip() else ''
            lowerbound = sympy.sympify(self.lboundEdit21.text()) if self.lboundEdit21.text().strip() else ''
            f = sympy.sympify(self.funcEdit2.toPlainText()) if self.funcEdit2.toPlainText().strip() else ''
            upperbound2 = sympy.sympify(self.uboundEdit22.text()) if self.uboundEdit22.text().strip() else ''
            lowerbound2 = sympy.sympify(self.lboundEdit22.text()) if self.lboundEdit22.text().strip() else ''
            self.latex_code = r'\iint_{'+sympy.latex(lowerbound)+'\leq x\leq '+sympy.latex(upperbound)+';'+sympy.latex(lowerbound2)+'\leq y\leq '+sympy.latex(upperbound2)+'}'+sympy.latex(f)+'\mathrm{d}x\mathrm{d}y'
            x = sympy.Symbol('x')
            y = sympy.Symbol('y')
            self.svgWidget2.close()
            self.ans=sympy.integrate(f, (x, lowerbound, upperbound),(y, lowerbound2, upperbound2)) if exchange else sympy.integrate(f, (y, lowerbound2, upperbound2),(x, lowerbound, upperbound))
        else:
            upperbound = sympy.sympify(self.uboundEdit31.text()) if self.uboundEdit31.text().strip() else ''
            lowerbound = sympy.sympify(self.lboundEdit31.text()) if self.lboundEdit31.text().strip() else ''
            f = sympy.sympify(self.funcEdit3.toPlainText()) if self.funcEdit3.toPlainText().strip() else ''
            upperbound2 = sympy.sympify(self.uboundEdit32.text()) if self.uboundEdit32.text().strip() else ''
            lowerbound2 = sympy.sympify(self.lboundEdit32.text()) if self.lboundEdit32.text().strip() else ''
            upperbound3 = sympy.sympify(self.uboundEdit33.text()) if self.uboundEdit33.text().strip() else ''
            lowerbound3 = sympy.sympify(self.lboundEdit33.text()) if self.lboundEdit33.text().strip() else ''
            self.latex_code = r'\iiint_{'+sympy.latex(lowerbound)+'\leq x\leq '+sympy.latex(upperbound)+';'+sympy.latex(lowerbound2)+'\leq y\leq '+sympy.latex(upperbound2)+';'+sympy.latex(lowerbound3)+'\leq z\leq '+sympy.latex(upperbound3)+'}'+sympy.latex(f)+'\mathrm{d}x\mathrm{d}y\mathrm{d}z'
            x = sympy.Symbol('x')
            y = sympy.Symbol('y')
            z = sympy.Symbol('z')
            self.svgWidget3.close()
            self.ans=sympy.integrate(f,(y, lowerbound2, upperbound2),(z, lowerbound3, upperbound3), (x, lowerbound, upperbound))
            if type(lowerbound)==type(x) or type(upperbound)==type(x):
                if type(lowerbound2)==type(x) or type(upperbound2)==type(x):
                    self.ans=sympy.integrate(f, (y, lowerbound2, upperbound2), (x, lowerbound, upperbound), (z, lowerbound3, upperbound3))
                else:
                    self.ans=sympy.integrate(f,(x, lowerbound, upperbound),(z, lowerbound3, upperbound3), (y, lowerbound2, upperbound2))

        self.close()
        print(self.ans)

    


# matplotlib: force computer modern font set
plt.rc('mathtext', fontset='cm')

#将tex公式渲染成SVG格式图片.入口参数：string formula为tex公式代码，fontsize为字号，dpi为分辨率，越小越清晰
def tex2svg(formula, fontsize=12, dpi=1):
    fig = plt.figure(figsize=(0.001, 0.001))
    fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

    output = BytesIO()
    fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                bbox_inches='tight', pad_inches=0.0)
    plt.close(fig)

    output.seek(0)
    return output.read()


'''
constants = {'e':sympy.E, 'pi':sympy.pi}
op = ['(', ')', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '+', '=','^']
function_handle = {'':lambda x:x, 'arccos':lambda x:sympy.acos(x), 'arcsin':lambda x:sympy.asin(x), 'arctan':lambda x:sympy.atan(x), 'sin':lambda x:sympy.sin(x), 'cos':lambda x:sympy.cos(x), 'tan':lambda x:sympy.tan(x), 'lg':lambda x:sympy.log(x,10), 'ln':lambda x:sympy.log(x), 'sqrt()':lambda x:sympy.sqrt(x), 'x!':lambda x:sympy.factorial(x), '|x|':lambda x:sympy.Abs(x), 'exp':lambda x:sympy.exp(x)}
functions = ['sin', 'cos', 'tan', 'lg', 'ln', 'sqrt', 'fac', 'arcsin', 'arccos', 'arctan', 'abs', 'exp']
operators = ['arcsin', 'arccos', 'sin', 'cos', 'tan', 'arctan', 'lg', 'ln', '(', ')', 'exp', '^', '/', 'sqrt', '*', '-', 'abs', '+']
#将一个含变量的字符串转译成sympy表达式
def str2sym(List):
    CAL=[]
    FUNC=[]
    EXP=expression()
    CAL.append(EXP)
    for sender in List:
        if sender in constants.keys():   #按下的是pi或e等常量
            CAL[-1].curr_num=constants[sender]

        elif sender in functions:   #遇到函数
            temp=expression()           #新开一个expression对象压入CAL栈
            CAL.append(temp)            
            FUNC.append(sender)         #将函数记录到函数栈里面

        elif sender in op:  #如果按下的是运算符
            if sender=="(":    #新开一个expression类压入CAL栈,同时函数栈压入空字符串
                temp=expression()
                CAL.append(temp)
                FUNC.append("")

            elif sender[0].isdigit(): #如果是数字，直接读成浮点数
                CAL[-1].curr_num=float(sender) if '.' in sender else int(sender)

            elif (sender=="+" or sender=="-" or sender==")" or sender=="="):    #遇到+-)=，进行计算
                if (CAL[-1].base_num!=None):                                #结算^运算
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

                if sender ==")":
                    temp=CAL[-1].res
                    CAL.pop()
                    CAL[-1].curr_num=function_handle[FUNC[-1]](temp)
                    FUNC.pop()

            elif (sender=="*" or sender=="/"):  #遇到*/，记录在prev_sym和prev_num中                
                if (CAL[-1].base_num!=None):                                #结算^运算
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

            elif (sender=="^"): #遇到^，
                if (CAL[-1].base_num!=None):                                #结算^运算
                    CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
            
                CAL[-1].base_num=CAL[-1].curr_num
                CAL[-1].curr_num=None

    if (CAL[-1].base_num!=None):                                #结算^运算
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
    # CAL[-1].curr_num_text=""

    return CAL[0].res
'''
