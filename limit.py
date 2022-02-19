'''
本文件中定义lim类，是calculator界面"极限"选项卡弹窗的实现
'''

import sympy
from PyQt5.QtWidgets import (QWidget, QLabel, QAction, QLineEdit, QTextEdit, QGridLayout, QApplication, QStackedWidget, QPushButton, QMainWindow)
from PyQt5 import QtSvg
from PyQt5.QtCore import *
from str2svg import tex2svg
import sys
class lim(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)

        label1 = QLabel("极限过程：x→")
        label1.setAlignment(Qt.AlignCenter)
        grid.addWidget(label1, 0, 0)

        self.process = QLineEdit()
        grid.addWidget(self.process, 0, 1)

        label2 = QLabel("函数f(x)")
        label2.setAlignment(Qt.AlignCenter)
        grid.addWidget(label2, 1, 0, 2, 1)

        self.func = QTextEdit()
        grid.addWidget(self.func, 1, 1, 2, 1)

        self.svgWidget = QtSvg.QSvgWidget()
        grid.addWidget(self.svgWidget, 3, 0, 5, 2)

        preview = QPushButton("预览")
        confirm = QPushButton("确认")
        preview.clicked.connect(self.Render)
        confirm.clicked.connect(self.Conf)
        grid.addWidget(preview, 9, 0)
        grid.addWidget(confirm, 9, 1)

        self.setWindowTitle('输入极限')   
        self.show()

    def Render(self):
        p = sympy.latex(sympy.sympify(self.process.text())) if self.process.text().strip() else ''
        f = sympy.latex(sympy.sympify(self.func.toPlainText())) if self.func.toPlainText().strip() else ''
        latex_code = r'\lim_{x\to '+p+'}'+f
        self.svgWidget.load(tex2svg(latex_code,1))
        self.svgWidget.show()
        self.svgWidget.setFixedHeight(40)
        
    def Conf(self):
        return None


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = lim()
    sys.exit(app.exec_())