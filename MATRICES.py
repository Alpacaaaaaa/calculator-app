'''
矩阵运算界面的实现。
更新矩阵结果的显示。我对谱分解的结果进行判断，如果太复杂了就数值表示，比较简单就解析表示。这样能有效避免结果太长。虽然还是很长。因此，我又把界面调大了，勉强能放得下矩阵结果。谱分解暂时算搞定了，后期再优化吧
问题：SVD分解（数学部分还没搞定。可能只能数值解了）；LU分解，数学部分还没搞定，可能只能PLU
可能有bug
'''
import numpy as np
import sys
import sympy
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QAction, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap
from matrices_input import matrices_input
from str2svg import tex2svg
from PyQt5 import QtSvg
from mat2png import mat2png

class expression(): #表达式类，用来计算一个形如(a ± b */ c ^ d)的表达式的值。
    def __init__(self):
        self.res=None  #当前表达式中已经计算完了的部分，对应上面的a
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

style_sheet = "QPushButton{font-family:'Calibri Light';font-size:22px}\QPushButton{background-color:rgb(245,245,245)}\QPushButton{border:none}\QPushButton:hover{background-color:rgb(235, 235, 235)}"
MAT = {'A':None, 'B':None, 'C':None}
#异常处理函数，待完善
def ERROR_INPUT():
    return None

#矩阵运算函数
def SVD_construct(x,diag):
    u = None
    eigvecs2 = (x).eigenvects()
    eigvs2 = {a:c for (a,b,c) in eigvecs2}
    for _,ev in diag:
        for vec in eigvs2[ev]:
            if not u:
                u = sympy.Matrix(vec/vec.norm())
            else:
                u=u.col_insert(0,vec/vec.norm())
    return u
def SVD(x):
    sigma = v = u = None
    m,n = x.shape
    s = (x*x.T).eigenvals() if m<n else (x.T*x).eigenvals()
    a = x*x.T

    diag = {}
    # sympy.complex
    for i in s.keys():
        for j in range(s[i]):
            diag[i] = (sympy.simplify(sympy.Abs(i)).expand(complex = True))
    print(diag)
    diag = sorted(diag.items(), key = lambda x:x[1], reverse=False)
    print(diag)
    v = SVD_construct(x*x.T,diag)
    u = SVD_construct(x.T*x,diag)
    sigma = v.T*x*u.T
    return v,sigma,u
def inv(x):
    c,r = x.shape
    return x.inv() if c == r else x.pinv()
def EIG(x):
    if not x.is_diagonalizable():
        return None
    p,d = x.diagonalize()

    if 2*len(sympy.latex(p))+len(sympy.latex(d))>400 and d.shape != (2,2):
        p,d = p.evalf(n=4),d.evalf(n=4)
        ans = []
        for mat in [p,d]:
            m,n = mat.shape
            tmp = sympy.Matrix([[]])
            for i in range(m):
                row = mat.row(m-1-i)
                row_i = []
                for j in range(n):
                    row_i.append(sympy.re(row[j]) if sympy.im(row[j]) < 1e-4 else row[j])
                tmp = tmp.row_insert(0,sympy.Matrix(1,n,row_i))
            ans.append(tmp)
        return (False,ans[1],ans[0])
    return (False,d,p)
def LU(x):
    L,U,p = x.LUdecomposition()
    return L,U,sympy.eye(x.rows).permuteFwd(p)
#GUI界面
class mat_Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.restart=True   #restart标志量表示是否重开

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(3)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(250,250,250))
        self.setPalette(self.palette)

        #工具栏选项
        #“设置”选项卡
        minput = QAction('输入矩阵', self)
        minput.triggered.connect(self.show_input)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(minput)


        #初始化“设置”“积分”“极限”“级数和”选项卡
        self.input_dialog = matrices_input()
        self.input_dialog.Signal.connect(self.read_matrices)

        self.names = [('inv','逆或伪逆'), ('tran','转置'), ('det','行列式'), ('LU','LU分解'), ('QR','QR分解'), ('SVD','奇异值分解'), ('eig','谱分解'), ('NormF','Frobenius范数'),  '(', ')', 'CE', 'Bck',('trace','迹'), '8', '7', '9', ('A','调用矩阵A'), ('B','调用矩阵B'), ('Norm2','2-范数'), '4', '5', '6', '^', 'C', ('En','n阶单位阵'), '1', '2', '3', '*', '-', '', 'Ans', '0', '.', '+', '=']
        self.operators = ['(', ')', '7', '8', '9', '4', '5', '6', '*', '1', '2', '3', '-', '0', '+', '=', '^', '.']

        #利用lambda表达式给出函数对应的句柄，写成字典的形式，方便调用
        self.functions = {'':lambda x:x, 'SVD':lambda x: SVD(x), 'det':lambda x:x.det(), 'NormF':lambda x: x.norm(), 'inv':lambda x: inv(x), 'Norm2':lambda x: x.norm(2), 'En':lambda x: sympy.eye(x), 'trace':lambda x:x.trace(), 'tran':lambda x:x.T, 'QR':lambda x:x.QRdecomposition(), 'eig':lambda x:EIG(x), 'LU':lambda x:LU(x)}

        positions = [(i+20,j) for i in range(6) for j in range(6)]
        
        for position, name in zip(positions, self.names):   #对每个button设置位置、文字与快捷键
            if name == '':
                continue
            annotation = None
            if type(name) == tuple:
                name, annotation = name
            button=QPushButton(name,self)
            if name in self.operators:
                button.setShortcut(name)
            if annotation:
                button.setToolTip(annotation)

            button.clicked.connect(self.INPUT)
            button.setFixedSize(105,90)
            button.setStyleSheet(style_sheet)
            grid.addWidget(button, *position)
            button.pressed.connect(self.pressed_color)
            button.released.connect(self.released_color)

        #用于显示输入表达式的label
        self.exp=""
        self.label_exp = QLabel(self.exp, self)
        grid.addWidget(self.label_exp, 0, 0, 1, 6)
        self.label_exp.setAlignment(Qt.AlignRight|Qt.AlignBottom)
        self.label_exp.setFixedHeight(108)

        #用于显示计算结果的label
        self.label_ans = QLabel(self)
        grid.addWidget(self.label_ans, 10, 0, 1, 6)
        self.label_ans.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.label_ans.setFixedHeight(135)
        # self.svgWidget = QtSvg.QSvgWidget()
        # grid.addWidget(self.svgWidget, 10, 0, 1, 6, Qt.AlignRight)

        self.mem = []
        self.ans = None

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        self.setGeometry(300, 150,700 ,600)
        self.setWindowTitle('矩阵计算')
        self.show()

    #button被按下事件处理函数
    def INPUT(self):
        global CAL

        if self.restart:    #如果需要重开，则清除CAL栈
            CAL.clear()
            FUNC.clear()
            EXP=expression()
            CAL.append(EXP)
            self.restart=False
            self.exp=""
            self.mem.clear()
        
        sender=self.sender().text() #判断按下了哪个button
        if sender == "CE":
            self.restart=True
            self.label_exp.setText("")
            # self.label_ans.setText("")
            self.mem.clear()
            return None

        elif sender == "Bck":
            if len(self.mem)>0:
                self.mem.pop()
            self.compute(self.mem)
        else:
            self.mem.append(sender)
            self.compute(self.mem)

    def compute(self,LIST): #传入一个list对象——也就是self.mem，根据这个list对象解析出有效的表达式并计算
        if not LIST:
            self.label_exp.setText("")
            self.label_ans.setPixmap(QPixmap(''))
            self.label_ans.setText("")
            return None
        self.exp=""
        CAL.clear()
        FUNC.clear()
        EXP=expression()
        CAL.append(EXP)
        error_flag = False

        placeholder = ['flag', '_)']    #定义占位符列表.相比于一个有效的计算表达式，一个只输入了一半的表达式缺少了1.结尾处若干个匹配的右括号2.结尾的'='.因此，这里把这些缺少的都补上，这样就可以让输入一半的表达式变有效
        if LIST[-1]!='=':
            for i in range(LIST.count('(')-LIST.count(')')):
                LIST.append('_)')       #'_)'对应右括号，这里把括号全部匹配
            LIST.append('flag')         #'flag'对应'='

        for sender in LIST:
            if sender == 'Ans':
                CAL[-1].curr_num=self.ans
                self.exp+=sender

            elif sender == 'A' or sender == 'B' or sender == 'C':
                CAL[-1].curr_num = MAT[sender]
                self.exp = self.exp + sender

            elif sender in self.functions.keys():   #遇到函数
                temp=expression()           #新开一个expression对象压入CAL栈
                CAL.append(temp)
                FUNC.append(sender)         #将函数记录到函数栈里面
                self.exp=self.exp+sender+'('

            elif sender in self.operators or sender in placeholder:  #如果按下的是运算符
                if not(sender in placeholder):
                    self.exp=self.exp+sender
                self.restart=False

                if sender=="(":    #新开一个expression类压入CAL栈,同时函数栈压入空字符串
                    temp=expression()
                    CAL.append(temp)
                    FUNC.append("")

                elif sender.isdigit() or sender == '.': #如果是数字或小数点，继续读
                    CAL[-1].curr_num_text+=sender

                elif (sender=="+" or sender=="-" or sender==")" or sender=="=" or sender in placeholder):    #遇到+-)=，进行计算
                    if (CAL[-1].curr_num is None):                                #先结算curr_num的读取
                        try:
                            CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else (1 if (CAL[-1].base_num!=None or CAL[-1].curr_sym=='*') else 0)
                        except:
                            error_flag = True

                    if not(CAL[-1].base_num is None):                                #再结算^运算
                        CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                        CAL[-1].base_num=None

                    sgn=-1 if (CAL[-1].prev_sym=="-") else 1

                    if CAL[-1].curr_sym=="" and CAL[-1].curr_num != 0:               #再结算*运算
                        CAL[-1].res = (CAL[-1].curr_num*sgn+CAL[-1].res) if CAL[-1].res else CAL[-1].curr_num*sgn

                    elif (CAL[-1].curr_sym=="*"):
                        CAL[-1].res = CAL[-1].res+sgn*CAL[-1].curr_num*CAL[-1].prev_num if CAL[-1].res else sgn*CAL[-1].curr_num*CAL[-1].prev_num

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
                            CAL[-1].curr_num=self.functions[FUNC[-1]](ans)
                            FUNC.pop()

                elif (sender=="*"):  #遇到*，记录在prev_sym和prev_num中
                    if (CAL[-1].curr_num is None):                                #先结算curr_num的读取
                        CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else 0
                    
                    if not(CAL[-1].base_num is None):                                #再结算^运算
                        CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                        CAL[-1].base_num=None

                    if CAL[-1].prev_num is None:
                        CAL[-1].prev_num=CAL[-1].curr_num

                    else:
                        if (CAL[-1].curr_sym=="*"):
                            CAL[-1].prev_num=CAL[-1].prev_num*CAL[-1].curr_num

                    CAL[-1].curr_sym=sender
                    CAL[-1].curr_num=None
                    CAL[-1].curr_num_text=""

                elif (sender=="^"): #遇到^，
                    if (CAL[-1].curr_num is None):                                #先结算curr_num的读取
                        CAL[-1].curr_num=sympy.sympify(CAL[-1].curr_num_text) if CAL[-1].curr_num_text!="" else 0
                    if not(CAL[-1].base_num is None):                                #再结算^运算
                        CAL[-1].curr_num=CAL[-1].base_num**CAL[-1].curr_num
                
                    CAL[-1].base_num=CAL[-1].curr_num
                    CAL[-1].curr_num=None
                    CAL[-1].curr_num_text=""
            elif type(sender)!=type(''):
                if type(sender)==tuple:
                    name, num = sender
                    CAL[-1].curr_num = num
                    self.exp = self.exp + name

        #输出结果与格式控制
        self.label_exp.setFont(QFont("Calibri Light", *(16,75)))
        if self.restart:
            self.label_exp.setText(self.exp)
            if error_flag:
                self.label_ans.setPixmap(QPixmap(''))
                self.label_ans.setText('错误')
            else:
                '''
                这里，sympy.latex生成的字符串是一个常规字符串，但是传到mat2png函数的需要是一个raw字符串...还不能用转义符把'\'转义掉。。
                故出此下策。LOL
                '''
                if type(CAL[0].res)==sympy.matrices.dense.MutableDenseMatrix:
                    latex_code = sympy.latex(CAL[0].res).split('}')[1]
                    latex_code = latex_code.split(r'\end')[0].replace(r'\\',r'\cr')
                    latex_code = r'$$\left[\matrix{' + latex_code + r'}\right]$$'
                    shape = CAL[0].res.shape
                    mat2png(latex_code, shape)
                    pix_map = QPixmap('ans.png')
                    self.label_ans.setPixmap(pix_map)
                elif type(CAL[0].res)==tuple:
                    res = list(CAL[0].res)
                    latex_code = r'$$'
                    w,h = (0,0)
                    for i in range(len(res)):
                        if res[i]:
                            latex = sympy.latex(res[i]).split('}',1)[1]
                            latex = latex.split(r'\end')[0].replace(r'\\',r'\cr')
                            latex = r'\left[\matrix{' + latex + r'}\right]'
                            latex_code = latex_code + latex
                            wi,hi = res[i].shape
                            w = w + wi
                            h = hi if hi>h else h
                        else:
                            latex = sympy.latex(res[-1]).split('}',1)[1]
                            latex = latex.split(r'\end')[0].replace(r'\\',r'\cr')
                            latex = r'\left[\matrix{' + latex + r'}\right]^{-1}'
                            latex_code = latex_code + latex
                            wi,hi = res[-1].shape
                            w = w + wi + 1
                            h = hi if hi>h else h
                    latex_code += r'$$'
                    mat2png(latex_code, (w,h))
                    pix_map = QPixmap('ans.png')
                    self.label_ans.setScaledContents(True)
                    pix_map.scaled(self.label_ans.size(),Qt.KeepAspectRatio)
                    self.label_ans.setPixmap(pix_map)

                else:
                    self.label_ans.setFont(QFont("Calibri Light", *(20,75)))
                    self.label_ans.setText('{0}'.format(CAL[0].res))
        else:
            self.label_ans.setFont(QFont("Calibri Light", *(16,75)))
            self.label_ans.setText(self.exp)
            self.label_exp.setText('')
        self.label_ans.update()
        while LIST[-1] in placeholder:
            LIST.pop()   

    def pressed_color(self):    #按下button时改变颜色
        self.sender().setStyleSheet("QPushButton{background-color:rgb(235,235,235)}\QPushButton{border:none}")

    def released_color(self):   #松开时恢复
        self.sender().setStyleSheet(style_sheet)

    def show_input(self):
        self.input_dialog.show()
    def integral_input(self):
        self.int_dialog.show()
    def read_matrices(self):
        name,mat = self.input_dialog.mat
        MAT[name] = mat

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = mat_Calculator()
    sys.exit(app.exec_())