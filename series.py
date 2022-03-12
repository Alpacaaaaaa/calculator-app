'''
本文件中定义series类，是calculator界面"级数和"选项卡弹窗的实现
<<<<<<< HEAD
=======
增加异常处理
>>>>>>> temp
'''

import sympy
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QMessageBox, QPushButton)
from PyQt5 import QtSvg
from PyQt5 import QtCore
from str2svg import tex2svg
from PyQt5.QtGui import QColor, QPalette
import sys

class series(QWidget):
    Signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(250,250,250))
        self.setPalette(self.palette)

        label1 = QLabel("求和首项")
        label1.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label1, 0, 0)

        self.term = QLineEdit()
        self.term.setPlaceholderText('输入整数')
        grid.addWidget(self.term, 0, 1)

        label3 = QLabel("求和末项")
        label3.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label3, 1, 0)

        self.term2 = QLineEdit()
        self.term2.setPlaceholderText('输入整数，或infty表示无穷')
        grid.addWidget(self.term2, 1, 1)

        label2 = QLabel("级数an")
        label2.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(label2, 2, 0, 2, 1)

        self.func = QTextEdit()
        self.func.setPlaceholderText('输入关于项数n的通项表达式')
        grid.addWidget(self.func, 2, 1, 2, 1)

        self.svgWidget = QtSvg.QSvgWidget()
        grid.addWidget(self.svgWidget, 4, 0, 6, 2, QtCore.Qt.AlignCenter)
        
        preview = QPushButton("预览")
        confirm = QPushButton("确认")
        preview.clicked.connect(self.Render)
        confirm.clicked.connect(self.Conf)
        grid.addWidget(preview, 10, 0)
        grid.addWidget(confirm, 10, 1)

        self.setWindowTitle('输入级数和')   

    def Render(self):
        try:
            p = sympy.latex(sympy.sympify(self.term.text())) if self.term.text().strip() else ''
            if self.term2.text()=='infty':
                q = '\infty'
            else:
                q = sympy.latex(sympy.sympify(self.term2.text())) if self.term2.text().strip() else ''
            f = sympy.latex(sympy.sympify(self.func.toPlainText())) if self.func.toPlainText().strip() else ''
            latex_code = r'\sum_{n= ' + p + '}^{ '+q+'}'+f
            self.svgWidget.load(tex2svg(latex_code,1))

            self.svgWidget.show()
            self.svgWidget.setFixedWidth(60)
            self.svgWidget.setFixedHeight(60)
        except:
            QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        
    def Conf(self):
        try:
            p = sympy.sympify(self.term.text()) if self.term.text().strip() else ''
            if self.term2.text()=='infty':
                q = sympy.oo
            else:
                q = sympy.sympify(self.term.text()) if self.term.text().strip() else ''
            f = sympy.sympify(self.func.toPlainText()) if self.func.toPlainText().strip() else ''
            self.latex_code = r'\sum_{n= ' + sympy.latex(p) + '}^{ ' + sympy.latex(q) +'}' + sympy.latex(f)
            n = sympy.Symbol('n')
            self.ans=sympy.Sum(f,(n,p,q)).doit()
            self.Signal.emit('1')
            self.close()
        except:
            QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)