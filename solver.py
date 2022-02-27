'''
本文件中定义solver类，是数值求解方程（组）的实现
优化输出格式
'''

import sympy
from PyQt5.QtWidgets import (QWidget, QLabel, QAction, QLineEdit, QTextEdit, QGridLayout, QApplication, QStackedWidget, QPushButton, QMainWindow)
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPalette
import sys
class solver(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(250,250,250))
        self.setPalette(self.palette)

        label1 = QLabel("待求解变量：")
        label1.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(label1, 0, 0)

        label2 = QLabel("待求解方程：")
        label2.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(label2, 0, 1, 1, 2)

        self.label3 = QLabel("解：")
        self.label3.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label3, 0, 3)

        self.func = []
        self.var = []
        self.roots = []
        self.ans = None
        for i in range(3):
            f = QLineEdit()
            f.setText('')
            f.setPlaceholderText('输入关于已输入变量的函数')
            self.grid.addWidget(f, i+1, 1, 1, 2)
            f.setVisible(False if i>0 else True)
            self.func.append(f)

            v = QLineEdit()
            v.setText('')
            v.setPlaceholderText('输入字母作为变量名')
            self.grid.addWidget(v, i+1, 0)
            v.setVisible(False if i>0 else True)
            self.var.append(v)

            root = QLabel()
            root.setAlignment(QtCore.Qt.AlignLeft)
            self.grid.addWidget(root, i+1, 3)
            self.roots.append(root)

        self.ADD = QPushButton("添加变量与方程")
        self.DEL = QPushButton("删除变量与方程")
        SOL = QPushButton("求解")
        self.ADD.clicked.connect(self.add)
        self.DEL.clicked.connect(self.Del)
        SOL.clicked.connect(self.sol)
        self.grid.addWidget(self.ADD, 9, 2)
        self.grid.addWidget(self.DEL, 9, 1)
        self.DEL.setEnabled(False)
        self.grid.addWidget(SOL, 9, 3)
        self.num = 0

        self.setWindowTitle('方程求解')   
        self.show()

    def add(self):
        self.num += 1
        self.func[self.num].setVisible(True)
        self.var[self.num].setVisible(True)
        self.func[self.num].setText('')
        self.var[self.num].setText('')
        self.roots[self.num].setText('')

        if self.num==1:
            self.DEL.setEnabled(True)
        elif self.num==2:
            self.ADD.setEnabled(False)

    def Del(self):
        self.func[self.num].setVisible(False)
        self.var[self.num].setVisible(False)
        self.roots[self.num].setText('')
        self.num -= 1

        if self.num==1:
            self.ADD.setEnabled(True)
        elif self.num==0:
            self.DEL.setEnabled(False)

    def sol(self):
        eq = []
        variables = []
        for i in range(self.num + 1):
            variables.append(sympy.Symbol(self.var[i].text()))
            eq.append(sympy.sympify(self.func[i].text()))
        self.ans = sympy.solve(eq, variables)
        if not self.ans:
            self.roots[0].setText('无解')
        elif type(self.ans)==list:
            self.curr_idx = 0
            self.label3.setText('解：（{0}/{1}）'.format(self.curr_idx+1,len(self.ans)))
            if type(self.ans[0])==tuple:
                tmp = list(self.ans[0])
                for i in range(self.num + 1):
                    self.roots[i].setText(self.var[i].text() + '={0}'.format(round(sympy.N(tmp[i].subs('e',sympy.E)),6)))
            else:
                self.roots[0].setText(self.var[0].text() + '={0}'.format(round(sympy.N(self.ans[0].subs('e',sympy.E)),6)))
        elif type(self.ans)==dict:
            self.label3.setText('解：（1/1）')
            for i in range(self.num + 1):
                self.roots[i].setText(self.var[i].text() + '={0}'.format(round(sympy.N(list(self.ans.values())[i]),6)))
    
    def keyPressEvent(self, e): #通过键盘PgUp/PgDn键控制多解的显示
        if type(self.ans)==list and len(self.ans)>0:
            flag = False
            if e.key() == QtCore.Qt.Key_PageUp:
                self.curr_idx = 1+self.curr_idx if self.curr_idx!=len(self.ans)-1 else 0
                flag = True
            elif e.key() == QtCore.Qt.Key_PageDown:
                self.curr_idx = self.curr_idx-1 if self.curr_idx!=0 else len(self.ans)-1
                flag = True
            if flag:
                self.label3.setText('解：（{0}/{1}）'.format(self.curr_idx+1,len(self.ans)))
                if type(self.ans[0])==tuple:
                    for i in range(self.num + 1):
                        self.roots[i].setText(self.var[i].text() + '={0}'.format(round(sympy.N(list(self.ans[self.curr_idx])[i].subs('e',sympy.E)),6)))
                else:
                    self.roots[0].setText(self.var[0].text() + '={0}'.format(round(sympy.N(self.ans[self.curr_idx].subs('e',sympy.E)),6)))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = solver()
    sys.exit(app.exec_())