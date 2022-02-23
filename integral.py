'''
输入定积分弹窗的实现
现存问题：对不合法表达式抛异常；三重积分积分顺序；界面太丑了！！！
最近优化：无穷积分解析解,svg图大小
'''
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QMenu, QAction, QLineEdit, QTextEdit, QGridLayout, QStackedWidget, QPushButton, QMainWindow)
from PyQt5 import QtSvg, QtCore
import sympy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget
from str2svg import tex2svg
inf = {'+infty':+sympy.oo, '-infty':-sympy.oo, 'infty':sympy.oo}
class IntFrame(QMainWindow):
    Signal = QtCore.pyqtSignal(str)
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
        self.uboundEdit.setPlaceholderText('输入实数或(±)infty表示无穷')
        self.lboundEdit = QLineEdit()
        self.lboundEdit.setPlaceholderText('输入实数或(±)infty表示无穷')
        self.funcEdit = QTextEdit()
        self.funcEdit.setPlaceholderText('输入关于x的函数')
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
        self.uboundEdit21.setPlaceholderText('输入表达式或±infty表示无穷')
        self.lboundEdit21 = QLineEdit()
        self.lboundEdit21.setPlaceholderText('输入表达式或±infty表示无穷')
        self.uboundEdit22 = QLineEdit()
        self.uboundEdit22.setPlaceholderText('输入表达式或±infty表示无穷')
        self.lboundEdit22 = QLineEdit()
        self.lboundEdit22.setPlaceholderText('输入表达式或±infty表示无穷')
        self.funcEdit2 = QTextEdit()
        self.funcEdit2.setPlaceholderText('输入关于x,y的函数')
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
        self.uboundEdit31.setPlaceholderText('输入表达式或±infty表示无穷')
        self.lboundEdit31 = QLineEdit()
        self.lboundEdit31.setPlaceholderText('输入表达式或±infty表示无穷')
        self.uboundEdit32 = QLineEdit()
        self.uboundEdit32.setPlaceholderText('输入表达式或±infty表示无穷')
        self.lboundEdit32 = QLineEdit()
        self.lboundEdit32.setPlaceholderText('输入表达式或±infty表示无穷')
        self.uboundEdit33 = QLineEdit()
        self.uboundEdit33.setPlaceholderText('输入表达式或±infty表示无穷')
        self.lboundEdit33 = QLineEdit()
        self.lboundEdit33.setPlaceholderText('输入表达式或±infty表示无穷')
        self.funcEdit3 = QTextEdit()
        self.funcEdit3.setPlaceholderText('输入关于x,y,z的函数')
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
            if self.uboundEdit.text() in inf:
                upperbound = sympy.latex(inf[self.uboundEdit.text()])
            else:
                upperbound = sympy.latex(sympy.sympify(self.uboundEdit.text())) if self.uboundEdit.text().strip() else ''
            if self.lboundEdit.text() in inf:
                lowerbound = sympy.latex(inf[self.lboundEdit.text()])
            else:
                lowerbound = sympy.latex(sympy.sympify(self.lboundEdit.text())) if self.lboundEdit.text().strip() else ''
            f = sympy.latex(sympy.sympify(self.funcEdit.toPlainText())) if self.funcEdit.toPlainText().strip() else ''
            latex_code = r'\int_{'+lowerbound+'}^{'+upperbound+'}'+f+'\mathrm{d}x'
            self.svgWidget1.load(tex2svg(latex_code,1))
            self.grid1.addWidget(self.svgWidget1,4,0,5,2,QtCore.Qt.AlignCenter)
            self.svgWidget1.show()
            self.svgWidget1.setFixedHeight(40)
            self.svgWidget1.setFixedWidth(80)

        elif self.stackedWidget.currentIndex() == 1:
            if self.uboundEdit21.text() in inf:
                upperbound = sympy.latex(inf[self.uboundEdit21.text()])
            else:
                upperbound = sympy.latex(sympy.sympify(self.uboundEdit21.text())) if self.uboundEdit21.text().strip() else ''
            if self.lboundEdit21.text() in inf:
                lowerbound = sympy.latex(inf[self.lboundEdit21.text()])
            else:
                lowerbound = sympy.latex(sympy.sympify(self.lboundEdit21.text())) if self.lboundEdit21.text().strip() else ''
            f = sympy.latex(sympy.sympify(self.funcEdit2.toPlainText())) if self.funcEdit2.toPlainText().strip() else ''
            if self.uboundEdit22.text() in inf:
                upperbound2 = sympy.latex(inf[self.uboundEdit22.text()])
            else:
                upperbound2 = sympy.latex(sympy.sympify(self.uboundEdit22.text())) if self.uboundEdit22.text().strip() else ''
            if self.lboundEdit.text() in inf:
                lowerbound2 = sympy.latex(inf[self.lboundEdit22.text()])
            else:
                lowerbound2 = sympy.latex(sympy.sympify(self.lboundEdit22.text())) if self.lboundEdit22.text().strip() else ''
            latex_code = r'\iint_{'+lowerbound+'\leq x\leq '+upperbound+';'+lowerbound2+'\leq y\leq '+upperbound2+'}'+f+'\mathrm{d}x\mathrm{d}y'
            self.svgWidget2.load(tex2svg(latex_code,1))
            self.grid2.addWidget(self.svgWidget2,6,0,5,2)
            self.svgWidget2.show()
            self.svgWidget2.setFixedHeight(40)

        else:
            if self.uboundEdit31.text() in inf:
                upperbound = sympy.latex(inf[self.uboundEdit31.text()])
            else:
                upperbound = sympy.latex(sympy.sympify(self.uboundEdit31.text())) if self.uboundEdit31.text().strip() else ''
            if self.lboundEdit31.text() in inf:
                lowerbound = sympy.latex(inf[self.lboundEdit31.text()])
            else:
                lowerbound = sympy.latex(sympy.sympify(self.lboundEdit31.text())) if self.lboundEdit31.text().strip() else ''
            
            f = sympy.latex(sympy.sympify(self.funcEdit3.toPlainText())) if self.funcEdit3.toPlainText().strip() else ''

            if self.uboundEdit32.text() in inf:
                upperbound2 = sympy.latex(inf[self.uboundEdit32.text()])
            else:
                upperbound2 = sympy.latex(sympy.sympify(self.uboundEdit32.text())) if self.uboundEdit32.text().strip() else ''
            if self.lboundEdit.text() in inf:
                lowerbound2 = sympy.latex(inf[self.lboundEdit32.text()])
            else:
                lowerbound2 = sympy.latex(sympy.sympify(self.lboundEdit32.text())) if self.lboundEdit32.text().strip() else ''
            
            if self.uboundEdit33.text() in inf:
                upperbound3 = sympy.latex(inf[self.uboundEdit33.text()])
            else:
                upperbound3 = sympy.latex(sympy.sympify(self.uboundEdit33.text())) if self.uboundEdit33.text().strip() else ''
            if self.lboundEdit.text() in inf:
                lowerbound3 = sympy.latex(inf[self.lboundEdit33.text()])
            else:
                lowerbound3 = sympy.latex(sympy.sympify(self.lboundEdit33.text())) if self.lboundEdit33.text().strip() else ''

            latex_code = r'\iiint_{'+lowerbound+'\leq x\leq '+upperbound+';'+lowerbound2+'\leq y\leq '+upperbound2+';'+lowerbound3+'\leq z\leq '+upperbound3+'}'+f+'\mathrm{d}x\mathrm{d}y\mathrm{d}z'
            self.svgWidget3.load(tex2svg(latex_code,1))
            self.grid3.addWidget(self.svgWidget3,8,0,5,2)
            self.svgWidget3.show()
            self.svgWidget3.setFixedHeight(35)
    
    def Conf(self):
        if self.stackedWidget.currentIndex()==0:
            if self.uboundEdit.text() in inf:
                upperbound = inf[self.uboundEdit.text()]
            else:
                upperbound = sympy.sympify(self.uboundEdit.text()) if self.uboundEdit.text().strip() else ''
            if self.lboundEdit.text() in inf:
                lowerbound = inf[self.lboundEdit.text()]
            else:
                lowerbound = sympy.sympify(self.lboundEdit.text()) if self.lboundEdit.text().strip() else ''
            
            f_text = self.funcEdit.toPlainText().replace('e^(','exp(')  #这里的目的是把'e^'全部用'exp'代替，否则可能有些无穷积分无法得到解析解
            while f_text.find('e^')!=-1:
                index = f_text.find('e^') + 2
                while f_text[index] not in ['+','-','*','/','^',')']:
                    if index+1 == len(f_text):
                        break
                    index += 1
                f_text = f_text[:index+1] + ')' + f_text[index+1:]
                f_text = f_text.replace('e^','exp(')
            f = sympy.sympify(f_text) if self.funcEdit.toPlainText().strip() else ''
            
            self.latex_code=r'\int_{'+sympy.latex(lowerbound)+'}^{'+sympy.latex(upperbound)+'}'+sympy.latex(f)+'\mathrm{d}x'
            x = sympy.Symbol('x')
            self.ans=sympy.integrate(f, (x, lowerbound, upperbound))
        elif self.stackedWidget.currentIndex()==1:
            exchange = not ('x' in self.uboundEdit22.text() + self.lboundEdit22.text())

            if self.uboundEdit21.text() in inf:
                upperbound = inf[self.uboundEdit21.text()]
            else:
                upperbound = sympy.sympify(self.uboundEdit21.text()) if self.uboundEdit21.text().strip() else ''
            if self.lboundEdit21.text() in inf:
                lowerbound = inf[self.lboundEdit21.text()]
            else:
                lowerbound = sympy.sympify(self.lboundEdit21.text()) if self.lboundEdit21.text().strip() else ''

            f_text = self.funcEdit2.toPlainText().replace('e^(','exp(')  #这里的目的是把'e^'全部用'exp'代替，否则可能有些无穷积分无法得到解析解
            while f_text.find('e^')!=-1:
                index = f_text.find('e^') + 2
                while f_text[index] not in ['+','-','*','/','^',')']:
                    if index+1 == len(f_text):
                        break
                    index += 1
                f_text = f_text[:index+1] + ')' + f_text[index+1:]
                f_text = f_text.replace('e^','exp(')
            f = sympy.sympify(f_text) if self.funcEdit2.toPlainText().strip() else ''

            if self.uboundEdit22.text() in inf:
                upperbound2 = inf[self.uboundEdit22.text()]
            else:
                upperbound2 = sympy.sympify(self.uboundEdit22.text()) if self.uboundEdit22.text().strip() else ''
            if self.lboundEdit22.text() in inf:
                lowerbound2 = inf[self.lboundEdit22.text()]
            else:
                lowerbound2 = sympy.sympify(self.lboundEdit22.text()) if self.lboundEdit22.text().strip() else ''

            self.latex_code = r'\iint_{'+sympy.latex(lowerbound)+'\leq x\leq '+sympy.latex(upperbound)+';'+sympy.latex(lowerbound2)+'\leq y\leq '+sympy.latex(upperbound2)+'}'+sympy.latex(f)+'\mathrm{d}x\mathrm{d}y'
            x = sympy.Symbol('x')
            y = sympy.Symbol('y')
            self.svgWidget2.close()
            self.ans=sympy.integrate(f, (x, lowerbound, upperbound),(y, lowerbound2, upperbound2)) if exchange else sympy.integrate(f, (y, lowerbound2, upperbound2),(x, lowerbound, upperbound))
        else:
            if self.uboundEdit31.text() in inf:
                upperbound = inf[self.uboundEdit31.text()]
            else:
                upperbound = sympy.sympify(self.uboundEdit31.text()) if self.uboundEdit31.text().strip() else ''
            if self.lboundEdit31.text() in inf:
                lowerbound = inf[self.lboundEdit31.text()]
            else:
                lowerbound = sympy.sympify(self.lboundEdit31.text()) if self.lboundEdit31.text().strip() else ''

            f_text = self.funcEdit3.toPlainText().replace('e^(','exp(')  #这里的目的是把'e^'全部用'exp'代替，否则可能有些无穷积分无法得到解析解
            while f_text.find('e^')!=-1:
                index = f_text.find('e^') + 2
                while f_text[index] not in ['+','-','*','/','^',')']:
                    if index+1 == len(f_text):
                        break
                    index += 1
                f_text = f_text[:index+1] + ')' + f_text[index+1:]
                f_text = f_text.replace('e^','exp(')
            f = sympy.sympify(f_text) if self.funcEdit3.toPlainText().strip() else ''

            if self.uboundEdit32.text() in inf:
                upperbound2 = inf[self.uboundEdit32.text()]
            else:
                upperbound2 = sympy.sympify(self.uboundEdit32.text()) if self.uboundEdit32.text().strip() else ''
            if self.lboundEdit32.text() in inf:
                lowerbound2 = inf[self.lboundEdit32.text()]
            else:
                lowerbound2 = sympy.sympify(self.lboundEdit32.text()) if self.lboundEdit32.text().strip() else ''

            if self.uboundEdit33.text() in inf:
                upperbound3 = inf[self.uboundEdit33.text()]
            else:
                upperbound3 = sympy.sympify(self.uboundEdit33.text()) if self.uboundEdit33.text().strip() else ''
            if self.lboundEdit33.text() in inf:
                lowerbound3 = inf[self.lboundEdit33.text()]
            else:
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
        self.Signal.emit('1')
        self.close()