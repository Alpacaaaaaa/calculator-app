'''
输入矩阵弹窗的实现
'''
import numpy as np
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QMenu, QAction, QLineEdit, QTextEdit, QGridLayout, QStackedWidget, QPushButton, QMainWindow, QMessageBox)
from PyQt5 import QtCore
import sympy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication

class matrics_input(QMainWindow):
    Signal = QtCore.pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('添加矩阵')

        # 创建界面
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(250,250,250))
        self.setPalette(self.palette)

        # 初始化菜单栏
        self.menubar = QMainWindow.menuBar(self)

        modemenu = QMenu('切换输入模式',self)
        mode1 = QAction('全部输入',self)
        mode2 = QAction('按元素输入',self)

        modemenu.addAction(mode2)
        modemenu.addAction(mode1)

        mode1.triggered.connect(self.int1)
        mode2.triggered.connect(self.int2)

        self.menubar.addMenu(modemenu)

        # 设置stackedWidget
        self.stackedWidget = QStackedWidget()
        self.Layout = QVBoxLayout(self.centralwidget)
        self.Layout.addWidget(self.stackedWidget)

        self.form1  = QWidget()
        self.setup1()

        self.form2  = QWidget()
        self.setup2()

        self.stackedWidget.addWidget(self.form2)
        self.stackedWidget.addWidget(self.form1)

        self.resize(500,300)
        self.show()
        
        self.fill = quick_fill()
        self.fill.Signal.connect(self.set_val)

    def int1(self):
        self.stackedWidget.setCurrentIndex(0)

    def int2(self):
        self.stackedWidget.setCurrentIndex(1)

    def setup1(self):
        self.grid1 = QGridLayout(self.form1)

        label1 = QLabel("输入矩阵维数：")
        label_col = QLabel("行：")
        label_row = QLabel("列:")
        set_dim = QPushButton('确定')
        set_dim.clicked.connect(self.set_dim1)
        self.col_edit = QLineEdit()
        self.col_edit.setText('3')
        self.row_edit = QLineEdit()
        self.row_edit.setText('3')
        self.grid1.addWidget(label1,0,0)
        self.grid1.addWidget(label_col,0,1)
        self.grid1.addWidget(self.col_edit,0,2)
        self.grid1.addWidget(label_row,0,3)
        self.grid1.addWidget(self.row_edit,0,4)
        self.grid1.addWidget(set_dim,0,5)

        self.table = None
        self.set_dim1()

        fill_in = QPushButton("填充")
        fill_in.clicked.connect(self.fill_in)
        self.grid1.addWidget(fill_in,2,3)

        clear = QPushButton('清除')
        clear.clicked.connect(self.clear)
        self.grid1.addWidget(clear,2,4)

        conf = QPushButton('确认')
        conf.clicked.connect(self.confirm)
        self.grid1.addWidget(conf,2,5)

    def setup2(self):
        grid2 = QGridLayout(self.form2)

        label1 = QLabel('请输入矩阵：')
        self.mat_edit = QTextEdit()
        self.mat_edit.setPlaceholderText('每个元素之间用空格或逗号（英语）分隔，每行之间用回车或分号（英语）分隔')
        grid2.addWidget(label1,0,0,1,6)
        grid2.addWidget(self.mat_edit,1,0,10,6)

        conf = QPushButton('确认')
        conf.clicked.connect(self.confirm)
        grid2.addWidget(conf,11,5)


        return None

    def confirm(self):
        try:
            if self.stackedWidget.currentIndex()==1:
                vec1d = np.array([sympy.sympify(i.text()) for i in self.vec])
                self.mat = vec1d.reshape(int(self.col_edit.text()),int(self.row_edit.text()))
            else:
                TEXT = self.mat_edit.toPlainText()

                TEXT = TEXT.split('\n') if '\n' in TEXT else TEXT.split(';')
                a = ' ' if ' ' in TEXT[0] else ','
                self.mat = np.array([sympy.sympify(i) for i in TEXT[0].split(a)]).reshape(1,len(TEXT[0].split(a)))
                for i in range(len(TEXT)-1):
                    a = ' ' if ' ' in TEXT[i+1] else ','
                    self.mat = np.insert(self.mat,i+1,values = [sympy.sympify(num) for num in TEXT[i+1].split(a)], axis = 0)
            self.Signal.emit('ready')
        except:
            QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)

    def set_dim1(self):     #设置矩阵维度，并更新输入框表格
        if self.table:
            self.table.deleteLater()
        self.vec = []
        self.table = QWidget()
        grid = QGridLayout(self.table)
        positions = [(i,j) for i in range(int(self.col_edit.text())) for j in range(int(self.row_edit.text()))]
        for p in positions:
            le = QLineEdit()
            le.setPlaceholderText('({0},{1})分量'.format(list(p)[0]+1,list(p)[1]+1))
            grid.addWidget(le,*p)
            self.vec.append(le)

        self.grid1.addWidget(self.table,1,0,1,6)

    def clear(self):    #将所有元素清空
        for le in self.vec:
            le.setText('')

    def fill_in(self):
        self.fill.show()
        return None
    
    def set_val(self):
        for le in self.vec:
            if le.text() == '':
                le.setText(str(self.fill.value))

class quick_fill(QWidget):  #快捷填充弹窗的实现
    Signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(250,250,250))
        self.setPalette(self.palette)

        label = QLabel('将所有尚未输入的元素置为指定的值：')
        grid.addWidget(label,0,0,1,4)

        self.val = QLineEdit()
        self.val.setText('0')
        grid.addWidget(self.val,1,0,1,4)
        
        conf = QPushButton('确认')
        conf.clicked.connect(self.conf)
        grid.addWidget(conf,2,3)

        canc = QPushButton('取消')
        canc.clicked.connect(self.canc)
        grid.addWidget(canc,2,2)

        self.setWindowTitle('快速填充')    

    def canc(self):
        self.val.setText('0')
        self.close()

    def conf(self):
        try:
            self.value = sympy.sympify(self.val.text().replace(' ',''))
            self.Signal.emit('1')
            self.close()
        except:
            QMessageBox.warning(self, "Warning", "不合法的输入！", QMessageBox.Ok)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = matrics_input()
    sys.exit(app.exec_())